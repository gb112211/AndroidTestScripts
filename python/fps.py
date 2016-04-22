#!/usr/bin/env python
# -*- coding: utf-8 -*

__author__ = 'xuxu'

import time
import os
import sys

from scriptUtils import utils

PATH = lambda p: os.path.abspath(p)

class SurfaceFlinger(object):

    CLEAR_BUFFER_CMD = "dumpsys SurfaceFlinger --latency-clear"
    FRAME_LATENCY_CMD = "dumpsys SurfaceFlinger --latency"
    PAUSE_LATENCY = 20  #两个frame之间的latency大于20，则不是一个jankniess
    PENDING_FENCE_TIME = (1 << 63) - 1  #Symbol of unfinished frame time

    refresh_period = -1     #刷新周期
    frame_buffer_data = []
    frame_latency_data_size = 0
    max_Vsync = 0

    def __init__(self, activity_name, dump_time):
        """
        :param activity_name: 当前界面的"package/activity"
        :param dump_time: 每次获取SurfaceFlinger数据的时间间隔
        """
        self.activity_name = activity_name
        self.dump_time = dump_time

    #清除SurfaceFlinger缓存数据
    def __clear_buffer(self):
        results = utils.shell("{0} {1}".format(self.CLEAR_BUFFER_CMD, self.activity_name))\
            .stdout.readlines()
        return not len(results)

    #开始获取SurfaceFlinger数据
    def start_dump_latency_data(self, ignore_pending_fence_time = False):
        results = []
        if self.__clear_buffer():
            time.sleep(self.dump_time)
            results = utils.shell("{0} {1}".format(self.FRAME_LATENCY_CMD, self.activity_name))\
                .stdout.readlines()
            self.refresh_period = int(results[0].strip())

            if self.refresh_period < 0:
                return False

            data_invalid_flag = False
            for line in results:
                if not line.strip():
                    break

                if len(line.split()) == 1 or line.split()[0] == "0":
                    continue
                elif line.split()[1] == str(self.PENDING_FENCE_TIME):
                    if ignore_pending_fence_time:
                        data_invalid_flag = True
                    else:
                        return False

                self.frame_buffer_data.append(line.split())
                if not data_invalid_flag:
                    self.frame_latency_data_size += 1

            return True

    def get_frame_latency_data_size(self):
        return self.frame_latency_data_size

    def get_refresh_period(self):
        return self.refresh_period

    #获取Vsync增量数据
    def __get_delta_Vsync_data(self):
        delta_Vsync_data = []
        if self.frame_buffer_data:
            first_Vsync_time = long(self.frame_buffer_data[0][1])
            for i in xrange(0, self.frame_latency_data_size-1):
                cur_Vsync_time = long(self.frame_buffer_data[i+1][1])
                delta_Vsync_data.append(cur_Vsync_time - first_Vsync_time)
                first_Vsync_time = cur_Vsync_time
                if self.max_Vsync < delta_Vsync_data[i]:
                    self.max_Vsync = delta_Vsync_data[i]
        return  delta_Vsync_data

    #在delta_Vsync_data基础上再获取增量数据
    def __get_delta2_Vsync_data(self):
        delta_Vsync_data = self.__get_delta_Vsync_data()
        delta2_Vsync_data = []
        num_delta_Vsync = self.frame_latency_data_size - 1

        for i in xrange(0, num_delta_Vsync-1):
            delta2_Vsync_data.append(delta_Vsync_data[i+1] - delta_Vsync_data[i])
        return delta2_Vsync_data

    def __get_normalized_delta2_Vsync(self):
        delta2_Vsync_data = self.__get_delta2_Vsync_data()
        normalized_delta2_Vsync = []
        for i in xrange(0, self.frame_latency_data_size-2):
            normalized_delta2_Vsync.append(delta2_Vsync_data[i]/self.refresh_period)
        return normalized_delta2_Vsync

    def __get_round_normalized_delta2_Vsync(self):
        normalized_delta2_Vsync = self.__get_normalized_delta2_Vsync()
        round_normalized_delta2_Vsync = []
        for i in xrange(0, self.frame_latency_data_size-2):
            value = round(max(normalized_delta2_Vsync[i], 0.0))
            round_normalized_delta2_Vsync.append(value)

        return round_normalized_delta2_Vsync

    def get_Vsync_jankiness(self):
        if (self.refresh_period< 0):
            return -1
        round_normalized_delta2_Vsync = self.__get_round_normalized_delta2_Vsync()

        num_jankiness = 0
        for i in xrange(0, self.frame_latency_data_size-2):
            value = round_normalized_delta2_Vsync[i]
            if value > 0 and value < self.PAUSE_LATENCY:
                num_jankiness += 1

        return num_jankiness

    def get_max_delta_Vsync(self):
        return round(self.max_Vsync/self.refresh_period)

    def get_frame_rate(self):
        if self.refresh_period < 0:
            return -1
        if not self.frame_buffer_data:
            return -1
        start_time = long(self.frame_buffer_data[0][1])
        end_time = long(self.frame_buffer_data[-1][1])
        total_time = end_time - start_time
        return (self.frame_latency_data_size - 1) * 1e9 / total_time

    #停止数据采集
    def stop_dump_latency_data(self):
        self.refresh_period = -1
        self.frame_buffer_data = []
        self.frame_latency_data_size = 0
        self.max_Vsync = 0

def write_csv(*list):
    path = PATH("{}/fps_data".format(os.getcwd()))
    if not os.path.isdir(path):
        os.makedirs(path)
    f = open(PATH("%s/fps-%s.csv" %(path, utils.timestamp())), "w")
    times = list[0]
    fps = list[1]
    jankniess = list[2]

    for i in xrange(0, len(fps) - 1):
        f.write("{0},{1},{2},\n".format(str(times[i]), str(fps[i]), str(jankniess[i])))

    f.close()

if __name__ == "__main__":
    if not raw_input("Make sure the test Activity, in this process, you should keep in this Activity!\n"
              "Please press Enter continue..."):
        sleep_time = -1
        dump_time = -1
        while not 0 < sleep_time <= 10:
            try:
                sleep_time = float(raw_input("Please input sleep time(0-10s) :"))
            except:
                continue
        while dump_time < 0:
            try:
                dump_time = int(raw_input("Please input dump times: "))
            except:
                continue

        activity_name = utils.get_focused_package_and_activity()
        print "Current Activity: "
        print activity_name
        sf = SurfaceFlinger(activity_name, sleep_time)
        times = ["time"] + [i for i in xrange(1, dump_time+1)]
        jankniess = ["Jankniess"]
        fps = ["fps"]
        for i in xrange(0, dump_time):
            sf.start_dump_latency_data()
            frame= sf.get_frame_rate();
            if frame != -1:
                jankniess.append(sf.get_Vsync_jankiness())
                fps.append(frame)
            sf.stop_dump_latency_data()
        print "jankniess:"
        print jankniess
        print "fps:"
        print fps

        write_csv(times, fps, jankniess)

        raw_input("Please press Enter quit...")
        sys.exit(0)
