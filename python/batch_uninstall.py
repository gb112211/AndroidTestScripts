#!/usr/bin/python

import os
import sys

def uninstall():
    os.popen("adb wait-for-device")
    print "start uninstall..."
    for packages in os.popen("adb shell pm list packages -3").readlines():
        packageName = packages.split(":")[-1].splitlines()[0]
        os.popen("adb uninstall " + packageName)
        print "remove " + packageName + " successes."

if __name__ == "__main__":
    uninstall()
    print " "
    print "All the third-party applications uninstall successes."
