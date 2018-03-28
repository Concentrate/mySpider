import requests
import math
import time
import hashlib
import random
import threading


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


def testIpProxy():
    # 访问网址
    url = 'http://www.whatismyip.com.tw/'
    proxys = {"https:": "110.73.55.118",
              }
    a1, a2 = getASCP()
    req = requests.get(get_url(0, a1, a2), proxies=proxys)
    print(req.text)


class MyThread(threading.Thread):
    def __init__(self, name="default"):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        startRequestEffectient()


def startRequestEffectient():
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
    proxies = {}
    a1, a2 = getASCP()
    # aHeader["user-agent"] = random.choice(user_agent_list).strip()
    aHeader["user-agent"] = user_agent_list[0].strip()
    aHeader["cookie"] = "tt_webid={0}".format(random.choice(tt_webids)).strip()
    if random.random() < 0.5:
        proxies = {"https:": "https://" + random.choice(ip_proxies)}
    response = requests.get(get_url(0, a1, a2), headers=aHeader, proxies=proxies)
    # print(str(response.cookies) + "  :" + str(response.url))
    return response.json()


if __name__ == "__main__":
    # startRequestTest()
    thread_array = []
    for i in range(4):
        a1 = MyThread("thread {0}".format(i))
        a1.start()
        thread_array.append(a1)
    for tmp in thread_array:
        tmp.join()

    print("主线程退出")
