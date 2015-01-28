#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os
import sys

from scriptUtils import utils

#获取设备上当前应用的包名，结果存放于当前目录下的PackageName.txt中

PATH = lambda p: os.path.abspath(p)

if __name__ == "__main__":
    f = open(PATH("%s/PackageName.txt" %os.getcwd()), "w")
    f.write("Package: \n%s\n" %utils.get_current_package_name())
    f.close()
    print "Completed"
    sys.exit(0)
