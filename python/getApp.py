#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os

from scriptUtils import utils

#打开手机上的应用（包括系统应用），运行脚本，会将该应用对应的apk复制到本地的App文件夹下

PATH = lambda p: os.path.abspath(p)

def get_match_apk(package_name, path):
    list = []
    for packages in utils.shell("pm list packages -f %s" %package_name).stdout.readlines():
        if packages.split(":")[0] == "package":
            list.append(packages.split(":")[-1].split("=")[0])

    utils.adb("pull %s %s" %(list[0], path)).wait()

if __name__ == "__main__":
    path = PATH("%s/App" %os.getcwd())
    if not os.path.isdir(path):
        os.makedirs(path)

    get_match_apk(utils.get_current_package_name(), path)
    print "Completed"
    
