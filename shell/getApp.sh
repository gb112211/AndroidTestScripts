#!/bin/sh

#获取设备当前应用，存放于app目录下

#获取设备当前应用的包名
pkgname=`adb shell dumpsys window w | grep \/ | grep name= | cut -d = -f 3 | cut -d / -f 1`

#获取应用的apk路径
pkgpath=`adb shell pm list packages -f $pkgname | cut -d : -f 2 | cut -d = -f 1`

#apk存放目录
dir=app
if [ ! -d "$dir" ]
then
    mkdir $dir
fi

#pull apk
echo start pull $pkgname
`adb pull $pkgpath $dir`
echo Completed

