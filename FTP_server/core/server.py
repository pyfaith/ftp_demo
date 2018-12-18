#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import socketserver
import json
import configparser

STATUS_CODE = {
    250: "",
    251: "",
    252: "",
    253: "",
    254: "",
    255: "",
    256: "",
    250: "",
    250: "",
    250: "",
    250: "",
    250: "",
    250: "",
    250: "",
    250: "",
}


from conf import settings

class ServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        '''循环接受客服端数据'''

        while 1:
            data = self.request.recv(1024).decode("utf8").strip()
            data = json.loads(data)
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
                print("用户验证成功")
                return user



