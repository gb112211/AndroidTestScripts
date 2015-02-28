#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年2月28日

@author: xuxu
'''

import os

from scriptUtils import utils

#5037端口占用时杀掉占用该端口的进程

def linux():
    pid = os.popen("netstat -anop | grep 5037 | grep  LISTEN").read().split()[6].split("/")[0]
    os.system("kill %s" %pid)

def win():
    pid = os.popen("netstat -ano | findstr 5037 | findstr  LISTENING").read().split()[-1]
    os.system("taskkill /F /PID %s" %pid)
    

if __name__ == "__main__":
    if utils.system is "Windows":
        win()
    else:
        linux()