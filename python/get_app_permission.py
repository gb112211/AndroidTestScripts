#!/usr/bin/env python
# -*- coding=utf-8 -*-

from scriptUtils import utils

import json
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

PATH = lambda p: os.path.abspath(p)

# 获取设备上当前应用的权限列表
# Windows下会将结果写入permission.txt文件中，其他系统打印在控制台

def get_permission_list(package_name):

    permission_list = []
    result_list = utils.shell("dumpsys package %s | %s android.permission" %(package_name, utils.find_util)).stdout.readlines()

    for permission in result_list:
        permission_list.append(permission.strip())

    return permission_list

if __name__ == '__main__':
    package_name = utils.get_current_package_name()
    permission_list = get_permission_list(package_name)
    permission_json_file = file("permission.json")
    file_content = json.load(permission_json_file)["PermissList"]

    if utils.system is "Windows":
        f = open(PATH("%s/permission.txt" %os.getcwd()), "w")
        f.write("package: %s\n\n" %package_name)
        for permission in permission_list:
            for permission_dict in file_content:
                if permission == permission_dict["Key"]:
                    f.write(permission_dict["Key"] + ":\n  " + permission_dict["Memo"] + "\n")
        f.close
    else:
        print "package: %s\n" %package_name
        for permission in permission_list:
            for permission_dict in file_content:
                if permission == permission_dict["Key"]:
                    print permission_dict["Key"] + ":"
                    print "  " + permission_dict["Memo"]
