#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18

import socketserver


class ServerHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("ok")