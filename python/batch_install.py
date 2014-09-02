#coding=utf-8

#需要在脚本所在目录下有个AndroidAdb.exe程序，该adb可以支持安装以中文命名的apk
#需要将apk文件放在脚本所在目录下的Apps目录下

import os
import time
import sys

def check_adb():
    if os.path.isfile(os.getcwd() + "\\AndroidAdb\\AndroidAdb.exe"):
        return True
    else:
        return False

def check_dir():
    if os.path.isdir(os.getcwd() + "\\Apps"):
        return True
    else:
        return False

def install():
    count = 0
    for path, subdir, files in os.walk(os.getcwd() + "\\Apps"):
        for apk in files:
            os.system(os.getcwd() + "\\AndroidAdb\\AndroidAdb.exe install " + os.path.join(path, apk))
            count += 1

    print "\n" + str(count) + " apps install complete."

if __name__ == "__main__":
    if check_adb():
        pass
    else:
        print "AndroidAdb.exe not exist."
        time.sleep(5)
        sys.exit(1)

    if check_dir():
        pass
    else:
        print "Apps Directory not exist"
        time.sleep(5)
        sys.exit(1)

    install()
