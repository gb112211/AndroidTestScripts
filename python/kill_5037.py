# -*- coding: utf-8 -*-

'''
Created on 2015年2月28日

@author: xuxu
'''

import os
import platform

#5037端口占用时,打开该进程路径，且杀掉占用该端口的进程（只支持Windows）

def win():
    pid = os.popen("netstat -ano | findstr 5037 | findstr  LISTENING").read().split()[-1]
    process_name = os.popen('tasklist /FI "PID eq %s"' %pid).read().split()[-6]
    process_path = os.popen('wmic process where name="%s" get executablepath' %process_name).read().split()[-1]
    #分割路径，得到进程所在文件夹名
    name_list = process_path.split("\\")
    del name_list[-1]
    directory = "\\".join(name_list)
    #打开进程所在文件夹
    os.system("explorer.exe %s" %directory)
    #杀死该进程
    os.system("taskkill /F /PID %s" %pid)
    

if __name__ == "__main__":
    win()
