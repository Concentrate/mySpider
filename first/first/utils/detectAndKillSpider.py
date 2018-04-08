# -*- coding: utf-8 -*-

import os
import time
import datetime

detect_gap=10*60
max_memory=300*1000 #300m最大被允许


if __name__=="__main__":
    while True:
        find_memory_use_cmd="ps aux|grep toutiaoNewsSpider|awk '{print $6}'"
        res=os.popen(find_memory_use_cmd).readlines()
        is_kill=False
        for tmp in res:
            a1=int(tmp)
            if a1>=max_memory:
                is_kill=True
                break
        if is_kill:
            print("于{0} 杀掉爬虫进程，占用内存过大，准备重启...".format(datetime.datetime.now()))
            get_pid="ps aux|grep toutiaoNewsSpider|awk '{print $2}'"
            pids=os.popen(get_pid).readlines()
            for tmp in pids:
                print("进程id {0}".format(tmp))
                kill_cmd="kill -9 {0}".format(tmp)
                os.system(kill_cmd)
            print("准备重启爬虫")
            re_open_cmd="nohup python3 /home/ubuntu/spider/mySpider/first/first/spiders/toutiaoNewsSpiders.py &"
            os.system(re_open_cmd)
            print("重启进程成功")
        time.sleep(detect_gap)
