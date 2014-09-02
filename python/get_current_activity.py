#!/usr/bin/python

import os
import platform
import re
import sys

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")

def get_activity():
    os.popen("adb wait-for-device")
    out = os.popen("adb shell dumpsys input | " + find_util + " FocusedApplication").read()
    return pattern.findall(out)[0]


if __name__ == "__main__":
    f = open(PATH(os.getcwd() + "/CurrentActivity.txt"), "w")
    f.write("Activity: \n" + get_activity())
    f.close()
    sys.exit(0)
