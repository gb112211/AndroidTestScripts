#!/usr/bin/python
#coding=utf-8

import os
import sys

#卸载手机上的第三方应用

def uninstall():
    os.popen("adb wait-for-device")
    print "start uninstall..."
    for packages in os.popen("adb shell pm list packages -3").readlines():
        packageName = packages.split(":")[-1].splitlines()[0]
        os.popen("adb uninstall %s" %packageName)
        print "remove %s successes." %packageName

if __name__ == "__main__":
    uninstall()
    print " "
    print "All the third-party applications uninstall successes."
