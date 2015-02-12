#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年2月12日

@author: xuxu
'''

import os

from scriptUtils import utils

#adb backup命令可以备份，该脚本只用于备份设备上安装的第三方应用，将apk保存在当前目录下的backup_app文件夹中

PATH = lambda p : os.path.abspath(p)

def get_apk_list():
    apps = []
    for apk in utils.shell("pm list packages -f -3").stdout.readlines():
        apps.append(apk.split(":")[-1].split("=")[0])
        
    return apps

def backup_app():
    apps = get_apk_list()
    for apk in apps:
        utils.adb("pull %s backup_app" %apk).wait()
        print "pull %s succeed." %apk

if __name__ == "__main__":
    path = PATH("%s/backup_app" %os.getcwd())
    if not os.path.isdir(path):
        os.mkdir(path)
    backup_app()
    print "Completed"
