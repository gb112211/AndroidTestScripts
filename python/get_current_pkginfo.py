#!/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os
import tempfile

from scriptUtils import utils
from scriptUtils.exception import SriptException

#获取设备上当前应用的包信息，结果存放于当前目录下的PackageInfo.txt中

PATH = lambda p: os.path.abspath(p)
tempFile = tempfile.gettempdir()

def get_aapt():
    if "ANDROID_HOME" in os.environ:
        rootDir = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
        for path, subdir, files in os.walk(rootDir):
            if "aapt.exe" in files:
                return os.path.join(path, "aapt.exe")
            elif "aapt" in files:
                return os.path.join(path, "aapt")
    else:
        raise SriptException("ANDROID_HOME not exist")

def get_match_apk(package_name):
    list = []
    for packages in utils.shell("pm list packages -f %s" %package_name).stdout.readlines():
        list.append(packages.split(":")[-1].split("=")[0])
    apk_name = list[0].split("/")[-1]

    utils.adb("pull %s %s" %(list[0], tempFile)).wait()

    return PATH("%s/%s" %(tempFile, apk_name))

if __name__ == "__main__":
    package_name = utils.get_current_package_name()
    os.popen("%s dump badging %s > PackageInfo.txt" %(get_aapt(), get_match_apk(package_name)))
    # os.popen("del %s\\*.apk" %tempFile)
    print "Completed"
