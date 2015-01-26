#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os
import sys

from scriptUtils import utils

PATH = lambda p: os.path.abspath(p)


if __name__ == "__main__":
    f = open(PATH("%s/CurrentActivity.txt" %os.getcwd()), "w")
    f.write("Activity: \n%s" %utils.get_current_activity())
    f.close()
    print "Completed"
    sys.exit(0)