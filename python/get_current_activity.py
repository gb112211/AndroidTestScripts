#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os
import sys

from scriptUtils import utils

#获取设备上当前应用的“包名/Activity”，结果存放于当前目录下的CurrentActivity.txt

PATH = lambda p: os.path.abspath(p)

if __name__ == "__main__":
    f = open(PATH("%s/CurrentActivity.txt" %os.getcwd()), "w")
    f.write("Activity: \n%s\n" %utils.get_focused_package_and_activity())
    f.close()
    print "Completed"
    sys.exit(0)
