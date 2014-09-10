#!/usr/bin/python
#coding=utf-8

import os
import platform
import re
import sys

#获取设备当前界面的activity,保存至当前目录下的CurrentActivity.txt文件中

PATH = lambda p: os.path.abspath(p)

system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")

def get_activity():
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys window w | %s \/ | %s name=" %(find_util, find_util)).read()
    return pattern.findall(out)[0]


if __name__ == "__main__":
    f = open(PATH(os.getcwd() + "/CurrentActivity.txt"), "w")
    f.write("Activity: \n" + get_activity())
    f.close()
    sys.exit(0)
