# -*- coding:utf-8 -*-
import _thread
import os
import hashlib
import json
import math
import time
import sys
import os
import threading
import random
import pickle
import gc

moduleDir = "/home/ubuntu/spider/mySpider"
localModuleDir = "/Users/liudeyu/IdeaProjects/spiderPratise"
sys.path.append(moduleDir)
import requests

from first.first.utils import DataBaseUtil
from first.first.mails import sendMail


totalNum = 0;
sleepTimeSecond = 0.1;
threadLock = threading.Lock()
ttwebid_array=set()
topic="__all__"

user_agents_strs = '''
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
   Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11
       Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20
           Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52

    '''
user_agent_list = user_agents_strs.strip().split("\n")
tt_webids = [6441115964263679502, 6444852342776890893, 6469594619403077134, 6531538553481676296, 62996830351]
ip_proxies = ["110.73.55.118:8123", "58.19.81.54:18118", "123.180.69.170:8010", "101.37.79.125:3128",
                  "180.168.184.179:53128", "120.78.182.79:3128", "182.140.196.161:808", "114.215.95.188:3128",
                  "106.14.146.58:3128","219.135.164.245:3128","124.193.37.5:8888","118.212.137.135:31288",
                  "122.72.18.35:80","120.77.254.116:3128"]


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
    url = 'https://www.toutiao.com/api/pc/feed/?category={3}&utm_source=toutiao&widen=1' \
          '&max_behot_time={0}' \
          '&max_behot_time_tmp={0}' \
          '&tadrequire=true' \
          '&as={1}' \
          '&cp={2}'.format(max_behot_time, AS, CP,topic)
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
    global tt_webids,aHeader,ttwebid_array,user_agent_list,ip_proxies,ttwebid_array
    requests.adapters.DEFAULT_RETRIES=3;
    proxies = {}
    a1, a2 = getASCP()
    aHeader = {}
    thread_name=threading.current_thread().getName()
    index=thread_name[thread_name.find("-")+1:]
    index=int(index)
    aHeader["user-agent"] = user_agent_list[0].strip()
    if index<len(tt_webids):
           aHeader["cookie"] = "tt_webid={0}".format(tt_webids[1]).strip()
    if random.random() < 1.05 and index<len(ip_proxies):
        proxies = {"https:": "https://" + ip_proxies[index]}
    if index < len(user_agent_list):
        aHeader["user-agent"] = user_agent_list[index].strip()
    try:
        response = requests.get(get_url(0, a1, a2), headers=aHeader,proxies=proxies,timeout=5)
        #print(response.request.headers)
        #print(str(response.cookies) + "  :" + str(response.url))
        if response.cookies and response.cookies.get("tt_webid"):
            pass
            #ttwebid_array.add(response.cookies.get("tt_webid"))
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        time.sleep(2)
    return {}


def get_item(url):
    try:
        wbdata2 = getRequestJsonEffectient()
        if wbdata2 and wbdata2.get("message")!="success":
            #print("request not success")
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
    num=1
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
        num=num+1
        if num >=500:
            num=0
            gc.collect()


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

def initwebidsfile():
    global ttwebid_array
    filePath="/home/ubuntu/spider/mySpider/first/first/utils/webids_file"
    if os.path.exists(filePath):
        f1=open(filePath,"rb")
        ttwebid_array=pickle.load(f1)
        f1.close()
        print("初始化 ttwebids array and length is {0}".format(len(ttwebid_array)))

if __name__ == "__main__":
    initwebidsfile()
    if len(sys.argv)>=2:
        topic=sys.argv[1]
        print("topic 设置为 "+topic)
    threadCount = 5
    mThreadArray = []
    for i in range(threadCount):
        t1 = MyThread("thread-{0}".format(i))
        t1.start()
        mThreadArray.append(t1)

    for t2 in mThreadArray:
        t2.join()
