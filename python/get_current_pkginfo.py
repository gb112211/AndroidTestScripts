#coding=utf-8

import os
import tempfile
import re

#使用aapt获取设备上当前应用的apk信息，保存至当前目录下的PackageInfo.txt中

tempFile = tempfile.gettempdir()

def get_aapt():
    if "ANDROID_HOME" in os.environ:
        rootDir = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
        for path, subdir, files in os.walk(rootDir):
            if "aapt.exe" in files:
                return os.path.join(path, "aapt.exe")
    else:
        return "ANDROID_HOME not exist"

def get_current_package_name():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys window w | findstr \/ | findstr name=").read()
    package_name = pattern.findall(out)[0].split("/")[0]

    return package_name

def get_match_apk(package_name):
    list = []
    for packages in os.popen("adb shell pm list packages -f %s" %package_name).readlines():
        list.append(packages.split(":")[-1].split("=")[0])
    apk_name = list[0].split("/")[-1]
    os.popen("adb pull %s %s" %(list[0], tempFile))

    return tempFile + "\\" + apk_name

if __name__ == "__main__":
    os.popen(get_aapt() + \
             " dump badging %s > PackageInfo.txt" %get_match_apk(get_current_package_name()))
    os.popen("del %s\\*.apk" % tempFile)
