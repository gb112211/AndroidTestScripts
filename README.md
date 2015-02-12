AndroidTestScrpits
==================

Android测试中常用到的脚本

###主要脚本功能

批量安装应用（支持以中文命名的apk）、批量卸载、截屏、录制视频、获取当前应用的apk文件、包名、Activity名等。<br>

###2015.02.12
因日常工作需要，增加备份设备中安装的第三方应用的脚本backup_app.py。（区别于adb backup命令，只备份apk）<br>

###2015.01.31
修改screenrecord.py中的默认录制时间，默认最长录制时间为180秒<br>

###2015.01.29
新增脚本get_cpu_mem_info.py,获取设备当前运行的应用的cpu、memory信息，默认top times取值为20次，可自己修改脚本中的该参数

脚本运行需要安装pychartdir模块，安装方法请参考 [http://blog.csdn.net/gb112211/article/details/43272049](http://blog.csdn.net/gb112211/article/details/43272049 "python pychartdir模块的安装及使用")<br>
直接运行脚本，会生成线性图表存放于chart目录下，图表类似于：<br>
![image](image/cpu_mem_info.png "chart" )


###2015.01.28
修改了设备状态判断的代码（脚本自己都曾使用OK,如有问题，可以QQ联系：274925460）<br>

###2015.01.26

1.改写python分类中的脚本结构，将大部分方法分装进了scriptUtils包中的utils模块中<br>
2.新增screenrecord.py（录制视频,Android4.4新增功能）<br>
3.使用时请直接在脚本目录下运行脚本（可以将脚本目录复制到桌面上，使用时很方便）<br>
4.需要配置ANDROID_HOME，如果脚本执行失败，请在命令行模式下运行脚本，查看报错信息<br>
