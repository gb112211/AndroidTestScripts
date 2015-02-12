#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os

from scriptUtils import utils

#截取当前屏幕，截屏文件保存至当前目录下的screen文件夹中

PATH = lambda p: os.path.abspath(p)

def screenshot():
    path = PATH("%s/screenshot" %os.getcwd())
    utils.shell("screencap -p /data/local/tmp/tmp.png").wait()
    if not os.path.isdir(path):
        os.makedirs(path)
        
    utils.adb("pull /data/local/tmp/tmp.png %s" %PATH("%s/%s.png" %(path, utils.timestamp()))).wait()
    utils.shell("rm /data/local/tmp/tmp.png")   

if __name__ == "__main__":
    screenshot()
    print "success"
