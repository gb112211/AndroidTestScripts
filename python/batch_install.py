# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os
import time
import sys

#需要在脚本所在目录AndroidAdb目录下有个AndroidAdb.exe程序，该adb可以支持安装以中文命名的apk
#需要将apk文件放在脚本所在目录下的Apps目录下

#检查AndroidAdb.exe
def check_adb():
    if os.path.isfile("%s\\AndroidAdb\\AndroidAdb.exe" %os.getcwd()):
        return True
    else:
        return False

#检查Apps目录
def check_dir():
    if os.path.isdir("%s\\Apps" %os.getcwd()):
        return True
    else:
        return False

#安装应用
def install():
    count = 0
    apps_dir = "%s\\Apps" %os.getcwd()
    for path, subdir, files in os.walk(apps_dir):
        for apk in files:
            os.popen("%s\\AndroidAdb\\AndroidAdb.exe install %s" %(os.getcwd(), os.path.join(path, apk)))
            count += 1

    print "\n%s apps install complete." %str(count)

if __name__ == "__main__":
    if check_adb():
        pass
    else:
        print "AndroidAdb.exe not exist."
        time.sleep(3)
        sys.exit(0)

    if check_dir():
        pass
    else:
        print "Apps Directory not exist"
        time.sleep(3)
        sys.exit(0)

    install()
