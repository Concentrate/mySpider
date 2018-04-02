# -*- coding:utf-8 -*-
import atexit
import _thread
import hashlib
import json
import math
import time
import sys
import os
import threading
import random

moduleDir = "/home/ubuntu/spider/mySpider"
localModuleDir = "/Users/liudeyu/IdeaProjects/spiderPratise"
sys.path.append(moduleDir)
import requests

from first.first.utils import DataBaseUtil
from first.first.mails import sendMail


totalNum = 0;
sleepTimeSecond = 0;
threadLock = threading.Lock()


def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS, CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS, CP


def get_url(max_behot_time, AS, CP):
    url = 'https://www.toutiao.com/api/pc/feed/?category=__all__&utm_source=toutiao&widen=1' \
          '&max_behot_time={0}' \
          '&max_behot_time_tmp={0}' \
          '&tadrequire=true' \
          '&as={1}' \
          '&cp={2}&&_signature=T.8SGgAAFUyX-koALQErNk..Eg'.format(max_behot_time, AS, CP)
    return url


def printDataResult(data):
    global totalNum
    totalNum = totalNum + 1
    print("the {0}'s time data".format(totalNum))
    for news in data:
        title = news['title']
        news_url = news['source_url']
        news_url = "https://www.toutiao.com" + news_url
        print(title, news_url)


def getRequestJsonEffectient():
    user_agents_strs = '''
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
    '''

    #     110.73.55.118	8123	广西南宁	高匿	HTTPS	38天	2分钟前
    # Cn	58.19.81.54	18118	湖北武汉	高匿	HTTPS	1分钟	3分钟前
    # Cn	123.180.69.170	8010	河北邢台	高匿	HTTPS	1分钟	3分钟前
    # 101.37.79.125	3128		透明	HTTPS	230天	4分钟前
    # Cn	180.168.184.179	53128	上海	透明	HTTPS	58分钟	4分钟前
    # 120.78.182.79	3128	长城宽带	透明	HTTPS	4天	4分钟前
    # Cn	182.140.196.161	808	四川	高匿	HTTPS	3小时	4分钟前
    # Cn	114.215.95.188	3128	北京	透明	HTTPS	27天	4分钟前
    # 139.224.80.139	3128		透明	HTTPS	85天	4分钟前
    # Cn	122.72.18.34	80	甘肃	透明	HTTPS	194天	4分钟前
    # Cn	119.28.152.208	80	北京	透明	HTTPS	52天	4分钟前
    # Cn	114.215.47.93	3128	北京	透明	HTTPS	4小时	4分钟前
    # 106.14.146.58	3128		透明	HTTPS	6天	4分钟前
    # Cn	219.135.164.245	3128	广东广州市海珠区	透明	HTTPS	210天	4分钟前
    # Cn	119.28.138.104	3128	北京	高匿	HTTPS	11天	4分钟前
    # Cn	211.159.177.212	3128	北京	透明	HTTPS	66天	4分钟前
    # Cn	124.193.37.5	8888	北京	透明	HTTPS	7天	4分钟前
    # Cn	118.212.137.135	31288	江西	透明	HTTPS	50天	4分钟前
    # Cn	122.72.18.35	80	甘肃	透明	HTTPS	191天	4分钟前
    # 120.77.254.116	3128	长城宽带	透明	HTTPS	46天	4分钟前

    user_agent_list = user_agents_strs.strip().split("\n")
    tt_webids = [6441115964263679502, 6444852342776890893, 6469594619403077134, 6531538553481676296, 62996830351]
    ip_proxies = ["110.73.55.118:8123", "58.19.81.54:18118", "123.180.69.170:8010", "101.37.79.125:3128",
                  "180.168.184.179:53128", "120.78.182.79:3128", "182.140.196.161:808", "114.215.95.188:3128",
                  "106.14.146.58:3128"]
    aHeader = {
        # 6441115964263679502,6444852342776890893,6469594619403077134,6531538553481676296,62996830351
    }
    requests.adapters.DEFAULT_RETRIES=3;
    proxies = {}
    a1, a2 = getASCP()
    # aHeader["user-agent"] = random.choice(user_agent_list).strip()
    aHeader["user-agent"] = user_agent_list[0].strip()
    aHeader["cookie"] = "tt_webid={0}".format(random.choice(tt_webids)).strip()
    if random.random() < 0.5:
        proxies = {"https:": "https://" + random.choice(ip_proxies)}
    try:
        response = requests.get(get_url(0, a1, a2), headers=aHeader,proxies=proxies)
     #print(str(response.cookies) + "  :" + str(response.url))
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(e)
        time.sleep(3)
    return {}


def get_item(url):
    try:
        wbdata2 = getRequestJsonEffectient()
        if wbdata2 and wbdata2.get("message")!="success":
            # print("request not success")
            # print(wbdata2)
            global sleepTimeSecond
            time.sleep(sleepTimeSecond)
            return
        data = wbdata2.get("data")
        return data
    except Exception as e:
        print(e)
        # printDataResult(data)


def processData(data):
    DataBaseUtil.storeToutiaoNewsInDataBase(data)


def startRequest():
    while True:
        max_behot_time = 0
        AS, CP = getASCP()
        url = get_url(max_behot_time, AS, CP)
        data = get_item(url)
        if data and len(data) > 0:
            try:
                threadLock.acquire()
                processData(data)
            except Exception as e:
                print("处理数据时候异常,捕获")
            finally:
                threadLock.release()


def test_request(threadName, delay):
    AS, CP = getASCP()
    for i in range(10):
        text = requests.get(get_url(0, AS, CP), headers=aHeader).text
        print("thread name is {0} and the response is {1}".format(threadName, text))
        time.sleep(delay)


def testpalleryRequest():
    threadCount = 100
    for i in range(threadCount):
        _thread.start_new_thread(test_request, ("thread {0}".format(i), 1,))
    while True:
        time.sleep(5)


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        startRequest()
def atExit():
    print("主线程退出")
    localtime = time.asctime( time.localtime(time.time()))
    sendMail.sendNotifiedMessage("云服务器新闻爬虫进程结束 {0}".format(localtime),"爬虫相关")


if __name__ == "__main__":
    threadCount = 15
    mThreadArray = []
    for i in range(threadCount):
        t1 = MyThread("thread-{0}".format(i))
        t1.start()
        mThreadArray.append(t1)

    for t2 in mThreadArray:
        t2.join()
