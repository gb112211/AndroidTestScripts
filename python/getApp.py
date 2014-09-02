#!coding=utf-8

import os
import re

#打开手机上的第三方应用，运行脚本，会将该应用对应的apk复制到本地的Apps文件夹下

PATH = lambda p: os.path.abspath(p)

def get_current_package_name():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys input | findstr FocusedApplication").read()
    package_name = pattern.findall(out)[0].split("/")[0]

    return package_name

def get_match_apk(package_name, path):
    list = []
    for packages in os.popen("adb shell pm list packages -f " + package_name).readlines():
        list.append(packages.split(":")[-1].split("=")[0])
    apk_name = list[0].split("/")[-1]
    os.popen("adb pull " + list[0] + " " + path)

if __name__ == "__main__":
    path = PATH(os.getcwd() + "/Apps")
    if not os.path.isdir(PATH(os.getcwd() + "/Apps")):
        os.makedirs(path)

    get_match_apk(get_current_package_name(), path)
