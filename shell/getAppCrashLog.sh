#!/bin/sh

# 获取crash日志，存放至crash_log目录下

timestamp=`adb shell date +%F_%H-%M-%S | tr -d "\r"`
adb shell dumpsys dropbox | grep data_app_crash > temp.txt
log_dir="./crash_log"

if [ ! -d "$log_dir" ]
then
    mkdir $log_dir
fi

get_crash_log()
{
    time_list=[]
    index=0
    for result in `cat temp.txt | cut -d " " -f 2`
    do
        time_list[$index]=$result
        let "index+=1"
        
    done
   
    for time in ${time_list[@]}
    do
        adb shell dumpsys dropbox --print $time >> $log_dir/$timestamp.log
    done
}

get_crash_log
rm -f temp.txt
echo "Completed..."

