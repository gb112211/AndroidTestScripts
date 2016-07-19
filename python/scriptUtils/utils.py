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
import Tkinter  as tk
import ttk

import exception

serialno_num = ""

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


def get_screen_size(window):
    return window.winfo_screenwidth(),window.winfo_screenheight()

def get_window_size(window):
    return window.winfo_reqwidth(),window.winfo_reqheight()

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)

class Window(object):
    device_id = ""
    device_id_list = []
    root = None
    box = None
    def __init__(self, device_id_list, root):
        self.device_id_list = device_id_list
        self.device_id = device_id_list[0]
        self.root = root
        self.box = None

    def show_window(self):
        self.root.title(u'Serialno Number')
        center_window(self.root, 300, 240)
        self.root.maxsize(600, 400)
        self.root.minsize(300, 240)

        options = self.device_id_list
        self.box = ttk.Combobox(values=options)
        self.box.current(0)
        self.box.pack(expand = tk.YES)
        self.box.bind("<<ComboboxSelected>>", self.select)
        ttk.Button(text=u"确定", command=self.ok).pack(expand = tk.YES)

        self.root.mainloop()


    def select(self, event=None):
        self.device_id = self.box.selection_get()

    def ok(self):
        global serialno_num
        serialno_num = self.device_id
        self.root.destroy()

#adb命令
def adb(args):
    global serialno_num
    if serialno_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            #global serialno_num
            serialno_num = devices[0]
        else:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()    
    cmd = "%s -s %s %s" %(command, serialno_num, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#adb shell命令
def shell(args):
    global serialno_num
    if serialno_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serialno_num = devices[0]
        else:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()   
    cmd = "%s -s %s shell %s" %(command, serialno_num, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#获取设备状态
def get_state():
    return os.popen("adb -s %s get-state" %serialno_num).read().strip()

#获取对应包名的pid
def get_app_pid(pkg_name):
    if system is "Windows":
        string = shell("ps | findstr %s$" %pkg_name).stdout.read()

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

def get_device_list():
    devices = []
    result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result.reverse()
    for line in result[1:]:
        if "attached" not in line.strip():
            devices.append(line.split()[0])
        else:
            break
    return devices
    

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
