#!/usr/bin/python
#coding=utf-8

import os
import platform
import re
import sys

#获取当前应用的包名，保存至当前目录下的PackageName.txt文件中

PATH = lambda p: os.path.abspath(p)

system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")

def get_package_name():
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys window w | " + find_util + " \/ | " + find_util + " name=").read()
    package_name = pattern.findall(out)[0].split("/")[0]

    return package_name


if __name__ == "__main__":
    f = open(PATH(os.getcwd() + "/PackageName.txt"), "w")
    f.write("Package: \n" + get_package_name())
    f.close()
    sys.exit(0)
