#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pyfaith
# email: pyfaith@foxmail.com
# date: 18-12-18
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


IP = "127.0.0.1"
PORT = 1234

ACCOUNT_PATH = os.path.join(BASE_DIR, "conf", "accounts.cfg")