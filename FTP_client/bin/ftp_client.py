#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import optparse
import socket
import json


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
        if self.authenticate():
            pass

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
        print(response)






if __name__ == '__main__':
    ch = ClientHandler()

    ch.interactive()