# -*- coding: utf-8 -*-
import pickle
import time
import os
import requests
import threading
import math
import hashlib
import random

ttwebid_array=None
webids_file="/home/ubuntu/spider/mySpider/first/first/utils/webids_file"
num_limit=2000

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
def getRequestJsonEffectient():
    user_agents_strs = '''
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
    '''
    user_agent_list = user_agents_strs.strip().split("\n")
    aHeader = {
    }
    global ttwebid_array
    requests.adapters.DEFAULT_RETRIES=3;
    s = requests.session()
    s.keep_alive = False
    a1, a2 = getASCP()
    aHeader["user-agent"] = user_agent_list[0].strip()
    try:
        response = requests.get(get_url(0, a1, a2), headers=aHeader)
        #print(str(response.cookies) + "  :" + str(response.url))
        time.sleep(1)
        if response.cookies and response.cookies.get("tt_webid"):
            ttwebid_array.add(response.cookies.get("tt_webid"))
            print("len of set is {0}".format(len(ttwebid_array)))
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
            #print(wbdata2)
            return
        data = wbdata2.get("data")
        return data
    except Exception as e:
        print(e)
        # printDataResult(data)
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self);
    def run(self):
        global ttwebid_array
        global webids_file
        while True:
            print("开始存入文件...,{0}".format(ttwebid_array))
            f=open(webids_file,"wb")
            pickle.dump(ttwebid_array,f)
            f.close()
            print("存入完成")
            time.sleep(60)
            global num_limit
            if len(ttwebid_array)>num_limit:
                break

class startRequeThread(MyThread):
    def run(self):
        while True:
          a1,a2=getASCP()
          url=get_url(0,a1,a2)
          get_item(url)
          global num_limit
          if len(ttwebid_array)>num_limit:
             break
          time.sleep(1)


if __name__=="__main__":
    if os.path.exists(webids_file):
        f=open(webids_file,"rb")
        ttwebid_array=pickle.load(f)
        f.close()
        print("初始载入 为 {0}".format(ttwebid_array))
    thread_array=[]
    t1=MyThread()
    t1.start()
    for i in range(6):
        a2=startRequeThread()
        a2.start()
        thread_array.append(a2)
    for t in thread_array:
        t.join()
    t1.join()





