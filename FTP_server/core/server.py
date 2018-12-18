#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import socketserver
import json
import configparser
import os

from conf import settings



from conf import settings


STATUS_CODE = {
    250: """Invaild cmd format #eg: {"action": "get", "filename": "test.py", "size": "1234"}""",
    251: "Invaild cmd",
    252: "Invaild auth data",
    253: "Wrong username or password",
    254: "Passed authentication",
    255: "Filename doesn`t provided",
    256: "File doesn`t exist on server",
    257: "Ready to send file",
    258: "md5 verification",

    800: "the file exist, but not enough, is contnue?",
    801: "the file exist!",
    802: "Ready to receive datas",

    900: "md5 valdate success",
}

class ServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''循环接受客服端数据'''

        while 1:
            data = self.request.recv(1024).decode("utf8").strip()
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError as e: #非json数据 Y/N
                pass
            # data type
            # '''
            # {   "action": "auth",
            #     "username":'user1',
            #     "passwd": '123',
            # }
            # '''
            if data.get("action"):

                if hasattr(self, data.get("action")):
                    func = getattr(self, data.get("action"))
                    func(**data)
                else: #error
                    pass
            else:#error
                pass



    def send_response(self, status_code):
        response = {"status_code": status_code, "status_msg": STATUS_CODE[status_code],}
        self.request.sendall(json.dumps(response).encode("utf8"))

    def auth(self, **data):
        '''用户验证'''
        username = data["username"]
        password = data["password"]

        user = self.authenticate(username, password)

        if user:
            self.send_response(254)
        else:
            self.send_response(253)

    def authenticate(self, user, pwd):
        cfg = configparser.ConfigParser()
        cfg.read(settings.ACCOUNT_PATH)

        if user in cfg.sections():

            if pwd == cfg[user]["Password"]:
                self.user = user
                self.main_path = os.path.join(settings.BASE_DIR, "home", user)
                print("auth success:", user)
                return user


    def put(self, **data):
        '''接受客户端数据
        put 13.png iamges
        '''
        # print("put:", data)
        file_name = data.get("file_name")
        file_size = data.get("file_size")
        target_path = data.get("target_path")

        abs_path = os.path.join(self.main_path, target_path, file_name) #eg /home/faith/66.png

        ###################****************###########################
        #client 文件上传分析:
        '''
        client：
            用户输入：put test.mp4 testdir
                c1. 发送文件相关数句至server
                c2. server回应是否已有文件，有client询问用户是否续写：
                        是：回应server Y
                            续传文件
                        否： 回应server N
                            重新上传文件
                        
        
        
        server
                s1. 获取数据 data={'action':'put', 'filename': 'test.mp4'...}
                    判断本地是否有该文件存在：
                        是：
                            文件完整：   
                                s2. 回应client以有完整文件
                            文件不完整：  
                                s2. 回应client文件不完整，是否续传，等待client回应：
                                        Y：续写文件
                                        N： 重新文件
                                              
                        否： 
                            s2.回应客户端server没有该文件
                            直接写文件
        
        
        '''
        has_received = 0
        if os.path.exists(abs_path):
            file_has_size = os.stat(abs_path).st_size #获取本地存放文件的大小
            if file_has_size < file_size:#断点续传
                self.request.sendall("800".encode("utf8"))
                choice = self.request.recv(1024).decode("utf8")
                if choice == "Y": #用户需要续传文件
                    self.request.sendall(str(file_has_size).encode("utf8")) #告诉客户端本地已有文件的数据大小

                    f = open(abs_path, "ab")
                    has_received += file_has_size #重置 文件写 循环条件

                else: #用户不续传，重新复写文件
                    f = open(abs_path, "wb")


            else: #服务端文件是完整文件
                self.request.sendall("801".encode("utf8"))
                return ###>>>>>>self.handle

        else: #服务端没有该文件
            self.request.sendall("802".encode("utf8"))

            f = open(abs_path, "wb")

        #接受客户端发送过来的文件
        while has_received < file_size:
            try:
                data = self.request.recv(1024)
            except Exception as e:
                break
            f.write(data)
            has_received += len(data)
        f.close()

        ###################****************###########################





