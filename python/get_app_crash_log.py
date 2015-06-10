#!/usr/bin/env python
# -*- coding=utf-8 -*-

'''
Created on 2015年6月2日

@author: xuxu
'''

import os

from scriptUtils import utils

# app发生crash，未及时在logcat中抓取到有效log时，可通过该脚本获取到log，日志存放至crash_log目录

PATH = lambda p : os.path.abspath(p)

path = PATH("%s/crash_log" %os.getcwd())
if not os.path.isdir(path):
    os.mkdir(path)

# 获取app发生crash的时间列表
def get_crash_time_list():
    time_list = []
    result_list = utils.shell("dumpsys dropbox | %s data_app_crash" %utils.find_util).stdout.readlines()
    for time in result_list:
        temp_list = time.split(" ")
        temp_time= []
        temp_time.append(temp_list[0])
        temp_time.append(temp_list[1])
        time_list.append(" ".join(temp_time))

    return time_list

def get_crash_log(time_list):
    log_file = PATH("%s/crash_log/%s.txt" %(os.getcwd(), utils.timestamp()))
    f = open(log_file, "w")
    for time in time_list:
        cash_log = utils.shell("dumpsys dropbox --print %s" %time).stdout.read()
        f.write(cash_log)
    f.close()

if __name__ == '__main__':
   time_list = get_crash_time_list()
   get_crash_log(time_list)
   print "Completed"

