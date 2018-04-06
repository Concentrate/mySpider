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

moduleDir = "/home/ubuntu/spider/mySpider"
localModuleDir = "/Users/liudeyu/IdeaProjects/spiderPratise"
sys.path.append(moduleDir)
import requests

from first.first.utils import DataBaseUtil
from first.first.mails import sendMail


totalNum = 0;
sleepTimeSecond = 0;
threadLock = threading.Lock()
ttwebid_array=set()


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
          '&cp={2}'.format(max_behot_time, AS, CP)
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
                  "106.14.146.58:3128","219.135.164.245:3128","124.193.37.5:8888","118.212.137.135:31288",
                  "122.72.18.35:80","120.77.254.116:3128"]
    aHeader = {
        # 6441115964263679502,6444852342776890893,6469594619403077134,6531538553481676296,62996830351
    }
    global ttwebid_array
    requests.adapters.DEFAULT_RETRIES=3;
    s = requests.session()
    s.keep_alive = False
    proxies = {}
    a1, a2 = getASCP()
    aHeader["user-agent"] = user_agent_list[0].strip()
    ttwebid_str='''
uuid="w:5ffa14ae296f40f08229d3919c9a9730"; csrftoken=507bfea64d9314c23137a01b80e088fb; __utma=24953151.568239780.1499689176.1504956717.1504956717.1; _ba=BA0.2-20170715-51d9e-buvNklGp4n4PJ9h4DmPW; tt_webid={0}; WEATHER_CITY=%E5%8C%97%E4%BA%AC; _ga=GA1.2.568239780.1499689176; tt_webid={0}; UM_distinctid=160e54f3a82908-01c19ffad22fe2-32607402-13c680-160e54f3a839e8; odin_tt=e0c14af03526d18eb4fb451ef78f230f3b0c1fa374fb29ff92160302bb0783ea9540c0ffe87e43405b1ce929c81dfc24; utm_source=toutiao; tt_track_id=fda9fa9c847a29067d8638880d04cbba; login_flag=2f9f867b92bd3f46cc671bed03561c83; sessionid=2e37a104242cb6694be0a8e0fd3e1583; sid_tt=2e37a104242cb6694be0a8e0fd3e1583; uid_tt=61d884213e3e3fbc6255fdf91feaa727; sid_guard="2e37a104242cb6694be0a8e0fd3e1583|1522326884|15552000|Tue\054 25-Sep-2018 12:34:44 GMT"; sso_login_status=0; CNZZDATA1259612802=1561649699-1499685480-%7C1522986084; __tasessionId=0uicppx0z1522989236447
    '''
    thread_name=threading.current_thread().getName()
    index=thread_name[thread_name.find("-")+1:]
    index=int(index)
    if False and  len(ttwebid_array)!=0:
        aHeader["cookie"] = "tt_webid={0}".format(list(ttwebid_array)[index]).strip()
    else:
        if index<len(tt_webids):
           aHeader["cookie"] = "tt_webid={0}".format(tt_webids[index]).strip()
        else:
           aHeader["cookie"] = "tt_webid={0}".format(list(ttwebid_array)[-index]).strip()
    if random.random() < 1.8 and index<len(ip_proxies):
        proxies = {"https:": "https://" + ip_proxies[index]}
    try:
        #print(aHeader)
        response = requests.get(get_url(0, a1, a2), headers=aHeader,proxies=proxies)
        #print(str(response.cookies) + "  :" + str(response.url))
        if response.cookies and response.cookies.get("tt_webid"):
            pass
            #ttwebid_array.add(response.cookies.get("tt_webid"))
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(e)
        time.sleep(3)
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
    threadCount = 4
    mThreadArray = []
    filePath="/home/ubuntu/spider/mySpider/first/first/utils/webids_file"
    if os.path.exists(filePath):
        f1=open(filePath,"rb")
        ttwebid_array=pickle.load(f1)
        f1.close()
        print("初始化 ttwebids array and length is {0}".format(len(ttwebid_array)))
    for i in range(threadCount):
        t1 = MyThread("thread-{0}".format(i))
        t1.start()
        mThreadArray.append(t1)

    for t2 in mThreadArray:
        t2.join()
