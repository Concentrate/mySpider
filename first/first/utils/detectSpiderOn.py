# -*- coding: utf-8 -*-

import os
import time
import datetime
import time
re_open_times=1
gap=30*60;
def detect(tmp_list):
    for tmp in tmp_list:
        if tmp.find("python3")!=-1:
            return True
    return False
if __name__=="__main__":
    while True:
        print("进行爬虫进程存活检测")
        python_cmd="ps aux|grep toutiaoNewsSpider"
        res_list=os.popen(python_cmd).readlines()
        print(res_list)
        if res_list and len(res_list)>0:
            if not detect(res_list):
                re_open_spider="nohup python3 /home/ubuntu/spider/mySpider/first/first/spiders/toutiaoNewsSpiders.py >/dev/null 2>&1  &"
                os.system(re_open_spider)
                print("守护进程重新开启爬虫次数为 {0},当前时间为{1}".format(re_open_times,
                        datetime.datetime.now()))
                re_open_times=re_open_times+1
            else:
                print("爬虫已开启")
        time.sleep(gap)
        print("监测休眠...")

