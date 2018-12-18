#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import socketserver
import json

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

    def auth(self, **data):
        '''用户验证'''
        print("data", data)
