#!/usr/bin/env python
#coding=utf-8

'''
Created on 2019/5/30 10:24
@author: rikixu
'''

from scriptUtils import utils


def install(apkPath):
    print (utils.adb("install -r %s" %apkPath).stdout.read())


if __name__ == "__main__":
    apkPath = raw_input("apk path:")
    install(apkPath)