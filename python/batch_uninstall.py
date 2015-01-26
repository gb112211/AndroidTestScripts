#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os

#批量卸载设备上的应用

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