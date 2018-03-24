# -*- coding:utf-8 -*-
import requests
import json
import time
import math
import hashlib
import _thread

aHeader = {
    "cookie": '''
        uuid="w:5ffa14ae296f40f08229d3919c9a9730"; csrftoken=507bfea64d9314c23137a01b80e088fb; __utma=24953151.568239780.1499689176.1504956717.1504956717.1; uid_tt=0458becd862daec85c1fa9c16b09110d; _ba=BA0.2-20170715-51d9e-buvNklGp4n4PJ9h4DmPW; tt_webid=6441115964263679502; WEATHER_CITY=%E5%8C%97%E4%BA%AC; _ga=GA1.2.568239780.1499689176; tt_webid=6441115964263679502; UM_distinctid=160e54f3a82908-01c19ffad22fe2-32607402-13c680-160e54f3a839e8; odin_tt=e0c14af03526d18eb4fb451ef78f230f3b0c1fa374fb29ff92160302bb0783ea9540c0ffe87e43405b1ce929c81dfc24; utm_source=toutiao; tt_track_id=fda9fa9c847a29067d8638880d04cbba; sso_login_status=0; login_flag=2f9f867b92bd3f46cc671bed03561c83; sessionid=2e37a104242cb6694be0a8e0fd3e1583; sid_tt=2e37a104242cb6694be0a8e0fd3e1583; sid_guard="2e37a104242cb6694be0a8e0fd3e1583|1521618585|15552000|Mon\054 17-Sep-2018 07:49:45 GMT"; _gid=GA1.2.936302519.1521712193; __tasessionId=ccifqs4p81521859371997; CNZZDATA1259612802=1561649699-1499685480-%7C1521859526
        '''.strip(),
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}

totalNum = 0;
sleepTimeSecond = 1.5;


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


def get_item(url):
    wbdata = requests.get(url, headers=aHeader).content
    wbdata2 = json.loads(wbdata)
    if not "message" in wbdata2.keys() or wbdata2["message"] != "success":
        # print("request not success")
        print(wbdata2)
        global sleepTimeSecond
        time.sleep(sleepTimeSecond)
        return
    data = wbdata2.get("data")
    # printDataResult(data)
    return data


def processData(data):
    pass


def startRequest():
    while True:
        max_behot_time = 0
        AS, CP = getASCP()
        url = get_url(max_behot_time, AS, CP)
        data = get_item(url)
        if data and len(data) > 0:
            processData(data);

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


if __name__ == "__main__":
    startRequest()
