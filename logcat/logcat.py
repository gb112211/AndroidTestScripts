# coding=utf-8

'''
Created on 2016年1月21日

@author: xuxu
'''

#用法: logcat -v time

import sys
import os
import ctypes
import re

#输出类别标志
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

#颜色
"""

    0 = 黑色       8 = 灰色
    1 = 蓝色       9 = 淡蓝色
    2 = 绿色       A = 淡绿色
    3 = 浅绿色     B = 淡浅绿色
    4 = 红色       C = 淡红色
    5 = 紫色       D = 淡紫色
    6 = 黄色       E = 淡黄色
    7 = 白色       F = 亮白色
"""
BLACK = 0X00
RED = 0x0c
DARKRED = 0x40
BLUE = 0x09
GREEN = 0x0a
LIGHT_GREEN = 0x0b
YELLOW = 0x0e
WHITE = 0x0f
PINK = 0x0d

class Color(object):
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    
    def set_cmd_color(self, color, handle=std_out_handle):
        return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    
    def reset_color(self):
        self.set_cmd_color(RED | GREEN | BLUE)
    
    def show_verbose(self, msg):
        self.set_cmd_color(WHITE)
        sys.stdout.write(msg)
        self.reset_color()
        
    def show_debug(self, msg):
        self.set_cmd_color(LIGHT_GREEN)
        sys.stdout.write(msg)
        self.reset_color()
    
    def show_info(self, msg):
        self.set_cmd_color(GREEN)
        sys.stdout.write(msg)
        self.reset_color()
        
    def show_warn(self, msg):
        self.set_cmd_color(YELLOW)
        sys.stdout.write(msg)
        self.reset_color()
        
    def show_error(self, msg):
        self.set_cmd_color(RED)
        sys.stdout.write(msg)
        self.reset_color()
    
    def show_fatal(self, msg):
        self.set_cmd_color(DARKRED)
        sys.stdout.write(msg)
        self.reset_color()
        
def main(argv):
    color = Color()
    command = ""
    if "-d" in argv:
        command = "adb logcat %s" %" ".join(argv[1:])
    else:
        command = "adb logcat -d %s" %" ".join(argv[1:])
    if "brief" in argv or "process" in argv or "time" in argv:
        while True:
            TAG = False
            lines = os.popen(command).readlines()
            os.popen("adb logcat -c")
         
            for line in lines:
                if re.search(r"beginning of", line):
                    pass
                elif re.search(r"V\/.+(\d+\):)", line):
                    color.show_verbose(line)
                elif re.search(r"D\/.+(\d+\):)", line):
                    color.show_debug(line)
                elif re.search(r"I\/.+(\d+\):)", line):
                    color.show_info(line)
                elif re.search(r"W\/.+(\d+\):)", line):
                    color.show_warn(line)
                elif re.search(r"E\/.+(\d+\):)", line):
                    color.show_error(line)
                elif re.search(r"F\/.+(\d+\):)", line):
                    color.show_fatal(line)
                elif re.search(r"or defaults", line):
                    color.show_info(line)
                    TAG = True
                else:
                    color.show_info(line)
            if TAG:
                break
    elif "thread" in argv:
        while True:
            TAG = False
            lines = os.popen(command).readlines()
            os.popen("adb logcat -c")
            
            if "invalid option" in lines[0]:
                for line in lines:
                    color.show_info(line)
                break;
            
            for line in lines:
                if re.search(r"beginning of", line):
                    pass
                elif re.search(r"V\(.+:.+\)", line):
                    color.show_verbose(line)
                elif re.search(r"D\(.+:.+\)", line):
                    color.show_debug(line)
                elif re.search(r"I\(.+:.+\)", line):
                    color.show_info(line)
                elif re.search(r"W\(.+:.+\)", line):
                    color.show_warn(line)
                elif re.search(r"E\(.+:.+\)", line):
                    color.show_error(line)
                elif re.search(r"F\(.+:.+\)", line):
                    color.show_fatal(line)
                elif re.search(r"or defaults", line):
                    color.show_info(line)
                    TAG = True
                else:
                    color.show_info(line)
            if TAG:
                break
    elif "threadtime" in argv:
        while True:
            TAG = False
            lines = os.popen(command).readlines()
            os.popen("adb logcat -c")
            
            if "invalid option" in lines[0]:
                for line in lines:
                    color.show_info(line)
                break;
            
            for line in lines:
                if re.search(r"beginning of", line):
                    pass
                elif re.search(r"\s+V\s+", line):
                    color.show_verbose(line)
                elif re.search(r"\s+D\s+", line):
                    color.show_debug(line)
                elif re.search(r"\s+I\s+", line):
                    color.show_info(line)
                elif re.search(r"\s+W\s+", line):
                    color.show_warn(line)
                elif re.search(r"\s+E\s+", line):
                    color.show_error(line)
                elif re.search(r"\s+F\s+", line):
                    color.show_fatal(line)
                elif re.search(r"or defaults", line):
                    color.show_info(line)
                    TAG = True
                else:
                    color.show_info(line)
            if TAG:
                break;
    elif "tag" in argv:
        while True:
            TAG = False
            lines = os.popen(command).readlines()
            os.popen("adb logcat -c")
            
            if "invalid option" in lines[0]:
                for line in lines:
                    color.show_info(line)
                break;
            
            for line in lines:
                if re.search(r"beginning of", line):
                    pass
                elif re.search(r"^V/\w+:", line):
                    color.show_verbose(line)
                elif re.search(r"^D/\w+:", line):
                    color.show_debug(line)
                elif re.search(r"^I/\w+:", line):
                    color.show_info(line)
                elif re.search(r"^W/\w+:", line):
                    color.show_warn(line)
                elif re.search(r"^E/\w+:", line):
                    color.show_error(line)
                elif re.search(r"^F/\w+:", line):
                    color.show_fatal(line)
                elif re.search(r"or defaults", line):
                    color.show_info(line)
                    TAG = True
                else:
                    color.show_info(line)
            if TAG:
                break;
    else:
        while True:
            TAG = False
            lines = os.popen(command).readlines()
            os.popen("adb logcat -c")
            
            if "invalid option" in lines[0]:
                for line in lines:
                    color.show_info(line)
                break;
         
            for line in lines:
                if re.search(r"beginning of", line):
                    pass
                elif re.search(r"V\/.+(\d+\):)", line):
                    color.show_verbose(line)
                elif re.search(r"D\/.+(\d+\):)", line):
                    color.show_debug(line)
                elif re.search(r"I\/.+(\d+\):)", line):
                    color.show_info(line)
                elif re.search(r"W\/.+(\d+\):)", line):
                    color.show_warn(line)
                elif re.search(r"E\/.+(\d+\):)", line):
                    color.show_error(line)
                elif re.search(r"F\/.+(\d+\):)", line):
                    color.show_fatal(line)
                elif re.search(r"or defaults", line):
                    color.show_info(line)
                    TAG = True
                else:
                    color.show_info(line)
            if TAG:
                break;
            
if __name__ == "__main__":
    try:
        main(sys.argv)
    except:
        Color().reset_color()