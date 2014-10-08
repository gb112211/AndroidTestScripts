#!/bin/sh

adb shell wait-for-device
echo start remove...

for package in `adb shell pm list package -3 | cut -d : -f 2 | tr -d "\r"`
do
	echo remove $package
	adb uninstall $package
done
