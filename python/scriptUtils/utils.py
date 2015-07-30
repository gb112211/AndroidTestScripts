#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年1月23日

@author: xuxu
'''

import os
import platform
import re
import subprocess
import time

import exception

#判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"
    
#判断是否设置环境变量ANDROID_HOME
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
    else:
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
else:
    raise EnvironmentError(
        "Adb not found in $ANDROID_HOME path: %s." %os.environ["ANDROID_HOME"])
    
#adb命令
def adb(args):
    cmd = "%s %s" %(command, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#adb shell命令
def shell(args):
    cmd = "%s shell %s" %(command, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#获取设备状态
def get_state():
    return os.popen("adb get-state").read().strip()

#获取对应包名的pid
def get_app_pid(pkg_name):   
    if system is "Windows":
        string = shell("ps | findstr %s$" %pkg_name).stdout.read()
    else:
        string = shell("ps | grep -w %s" %pkg_name).stdout.read()

    if string == '':
        return "the process doesn't exist."

    pattern = re.compile(r"\d+")
    result = string.split(" ")
    result.remove(result[0])

    return  pattern.findall(" ".join(result))[0]

#杀掉对应包名的进程
def kill_process(pkg_name):
    pid = get_app_pid(pkg_name)
    
    result = shell("kill %s" %str(pid)).stdout.read().split(": ")[-1]
    
    if result != "":
        raise exception.SriptException("Operation not permitted or No such process")

#获取设备上当前应用的包名与activity    
def get_focused_package_and_activity():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    out = shell("dumpsys window w | %s \/ | %s name=" %(find_util, find_util)).stdout.read()

    return pattern.findall(out)[0]

#获取当前应用的包名
def get_current_package_name():
    return get_focused_package_and_activity().split("/")[0]

#获取当前设备的activity
def get_current_activity():
    return get_focused_package_and_activity().split("/")[-1]

#时间戳
def timestamp():
    return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

#连接设备
# adb("kill-server").wait()
# adb("start-server").wait()
adb("wait-for-device")

if get_state() != "device":
    adb("kill-server").wait()
    adb("start-server").wait()
    
if get_state() != "device":
    raise exception.SriptException("Device not run")
    

if __name__ == "__main__":
    pass
