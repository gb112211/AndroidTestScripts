#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月28日

@author: xuxu
'''

#需要安装pychartdir模块，http://blog.csdn.net/gb112211/article/details/43272049

import string

from scriptUtils import utils
from pychartdir import *

PATH = lambda p: os.path.abspath(p)

#打开待测应用，运行脚本，默认times为20次（可自己手动修改次数），获取该应用cpu、memory占用率的曲线图，图表保存至chart目录下

#top次数
times = 20

#设备当前运行应用的包名
pkg_name = utils.get_current_package_name()

#获取cpu、mem占用
def top():
    cpu = []
    mem = []

    top_info = utils.shell("top -n %s | %s %s$" %(str(times), utils.find_util, pkg_name)).stdout.readlines()

    for info in top_info:
        #temp_list = del_space(info)
        temp_list = info.split()
        cpu.append(temp_list[2])
        mem.append(temp_list[6])
    
    return (cpu, mem)

#去除top信息中的空格，便于获取cpu、mem的值        
#def del_space(str):
#    temp_list1 = str.split(" ")
#    temp_list2 = []
#   
#    for str in temp_list1:
#        if str != "":
#           temp_list2.append(str)
#           
#    return temp_list2

#绘制线性图表，具体接口的用法查看ChartDirecto的帮助文档
def line_chart():
    data = top()
    cpu_data = []
    mem_data = []
    
    #去掉cpu占用率中的百分号，并转换为int型
    for cpu in data[0]:
        cpu_data.append(string.atoi(cpu.split("%")[0]))
    
    #去掉内存占用中的单位K，并转换为int型，以M为单位  
    for mem in data[1]:
        mem_data.append(string.atof(mem.split("K")[0])/1024)
    
    #横坐标
    labels = []
    for i in range(1, times + 1):
        labels.append(str(i))
    
    #自动设置图表区域宽度
    if times <= 50:
        xArea = times * 40
    elif 50 < times <= 90:
        xArea = times * 20
    else:
        xArea = 1800
        
    c = XYChart(xArea, 800, 0xCCEEFF, 0x000000, 1)
    c.setPlotArea(60, 100, xArea - 100, 650)
    c.addLegend(50, 30, 0, "arialbd.ttf", 15).setBackground(Transparent)
    
    c.addTitle("cpu and memery info(%s)" %pkg_name, "timesbi.ttf", 15).setBackground(0xCCEEFF, 0x000000, glassEffect())
    c.yAxis().setTitle("The numerical", "arialbd.ttf", 12)
    c.xAxis().setTitle("Times", "arialbd.ttf", 12)
    
    c.xAxis().setLabels(labels)
    
    #自动设置X轴步长
    if times <= 50:
        step = 1
    else:
        step = times / 50 + 1
    
    c.xAxis().setLabelStep(step)
    
    layer = c.addLineLayer()
    layer.setLineWidth(2)
    layer.addDataSet(cpu_data, 0xff0000, "cpu(%)")
    layer.addDataSet(mem_data, 0x008800, "mem(M)")
    
    path = PATH("%s/chart" %os.getcwd())
    if not os.path.isdir(path):
        os.makedirs(path)
    
    #图片保存至脚本当前目录的chart目录下
    c.makeChart(PATH("%s/%s.png" %(path, utils.timestamp())))
    
if __name__ == "__main__":
    print "Starting get top information..."
    line_chart()
    
    
    
    
