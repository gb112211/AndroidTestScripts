#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月26日

@author: xuxu
'''

import os
import string
import sys
import time

from scriptUtils import utils

#需要Android4.4及4.4以上版本，运行脚本后可录制设备上的操作，默认使用手机分辨率，手动设置录制时间。
#录制结果存放于当前目录下的video目录下

PATH = lambda p: os.path.abspath(p)

def record():
    utils.shell("rm -f /data/local/tmp/video.mp4")
    limit_time = raw_input("Please set the maximum recording time, in seconds.  Maximum is 180.\n")
    if limit_time == "":
        utils.shell("screenrecord --time-limit 180 /data/local/tmp/video.mp4")
    try:
        _limit_time = int(limit_time) + 1
    except:
        record()
    if 0 < _limit_time <= 180:
        utils.shell("screenrecord --time-limit %s /data/local/tmp/video.mp4" %limit_time).wait()
    else:
        print "Please set again!"
        record()


if __name__ == "__main__":
    sdk = string.atoi(utils.shell("getprop ro.build.version.sdk").stdout.read())
    if sdk < 19:
        print "sdk version is %s, less than 19!"
        sys.exit(0)
    else:
        record()
        print "Get Video file..."
        time.sleep(3)

        path = PATH("%s/video" %os.getcwd())
        if not os.path.isdir(path):
            os.makedirs(path)

        utils.adb("pull /data/local/tmp/video.mp4 %s"  %PATH("%s/%s.mp4" %(path, utils.timestamp())))
        print "Completed"
