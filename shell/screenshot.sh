#!/bin/sh

#截取设备屏幕，将解图保存至当前目录下的screens文件夹

time=`adb shell date +%F_%H:%M:%S | tr -d "\r"`
adb shell screencap -p data/local/tmp/$time

dir=screens

if [ ! -d "$dir" ]
then
	mkdir $dir
fi

adb pull data/local/tmp/$time $dir/${time}".png"
