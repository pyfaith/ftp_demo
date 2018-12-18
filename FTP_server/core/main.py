#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import optparse

import socketserver


from conf import settings
from core import server



class ArgvHandler(object):
    '''处理命令行参数
    eg: python server.py [start|restart|stop]
    '''

    def __init__(self):
        self.op = optparse.OptionParser() #解析命令行参数

        # self.op.add_option("-s",  "--server", dest="server")
        # self.op.add_option("-P",  "--port", dest="port")

        options, args = self.op.parse_args()
        # options.server #取值
        self.verfy_args(options, args)

    def verfy_args(self, options, args):
        '''命令行验证参数'''
        cmd = args[0] if len(args) else "null"
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            func(options, args)

    def start(self, options, args):
        '''启动服务'''
        s = socketserver.ThreadingTCPServer((settings.IP, settings.PORT), server.ServerHandler)
        print("start server....")
        s.serve_forever()

    def restart(self, options, args):
        '''重启服务'''
        pass


    def stop(self, options, args):
        '''停止服务'''
        pass
