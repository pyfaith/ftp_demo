#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import optparse
import socket
import json
import os

class ClientHandler(object):

    def __init__(self):
        self.op = optparse.OptionParser()

        self.op.add_option("-s", "--server", dest="server")
        self.op.add_option("-P", "--port", dest="port")
        self.op.add_option("-u", "--username", dest="username")
        self.op.add_option("-p", "--password", dest="password")

        self.options, self.args = self.op.parse_args()

        self.verify_args(self.options, self.args)

        self.make_connection()
        self.main_path = os.path.dirname(os.path.abspath(__file__))

    def verify_args(self, options, agrs):
        '''验证ip和port'''
        server = self.options.server
        port = self.options.port
        # username = self.options.username
        # password = self.options.passowrd
        if self.options.port is None or self.options.server is None:
            print("请检查您输入的服务器ip或port是否有误。")


        if int(port) > 0 and int(port)< 65535:
            return True
        else:
            print("port is in 0 - 65535")

    def make_connection(self):
        '''创建连接'''
        self.sock = socket.socket()
        self.sock.connect((self.options.server, int(self.options.port)))

    def interactive(self):
        '''开始用户交互'''
        print("begin to interactive ......")
        if self.authenticate():

            cmd_info = input("[{user}]".format(user=self.user)).strip() #eg put test.py testdir

            cmd_list = cmd_info.split()
            if hasattr(self, cmd_list[0]):
                func = getattr(self, cmd_list[0])
                func(*cmd_list)

    def put(self, *cmd_list):
        '''put af.png dirimages'''
        action, local_path, target_path = cmd_list
        local_path = os.path.join(self.main_path, local_path)
        file_name = os.path.basename(local_path)
        file_size = os.stat(local_path).st_size
        data = {
            "action": "put",
            "file_name": file_name,
            "file_size": file_size,
            "target_path": target_path,
        }
        self.sock.send(json.dumps(data).encode("utf8"))

        #接受服务端返回信息
        is_exists = self.sock.recv(1024).decode("utf8")
        # print(is_exists,"*********************")

        ###################****************###########################
        #文件上传
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
        has_sent=0
        if is_exists == "800": #文件不完整******
            ''''''
            choice = input("this file exist, but not enough, is conutine? [[Y/N or y/n]]").strip()
            if choice.upper() == "Y":
                self.sock.sendall("Y".encode("utf8"))

                continue_position = self.sock.recv(1024).decode("utf8") #获取服务端已有文件大小



            else:
                self.sock.sendall("N".encode("utf8"))

        elif is_exists == "801": #服务端文件存在，并且完整
            return


        f = open(local_path, "rb")
        while has_sent < file_size:
            data = f.read(1024)
            self.sock.sendall(data)
            has_sent += len(data)

        f.close()
        print("put success!")
        ###################****************###########################








    def authenticate(self):
        '''检查用户输入账号'''
        if self.options.username is None or self.options.password is None:
            username = input("username: ")
            password = input("password: ")
            return self.get_auth_result(username, password)

        return self.get_auth_result(self.options.username, self.options.password)

    def response(self):
        data = self.sock.recv(1024).decode("utf8")
        data = json.loads(data)
        return data

    def get_auth_result(self, user, pwd):
        '''验证用户账号'''
        data = {
            "action": "auth",
            "username": user,
            "password": pwd,
        }
        data = self.sock.send(json.dumps(data).encode("utf8"))
        response = self.response()

        if response["status_code"] == 254:
            self.user = user
            print(response["status_msg"])
            return True
        else:
            print(response)







if __name__ == '__main__':
    ch = ClientHandler()

    ch.interactive()