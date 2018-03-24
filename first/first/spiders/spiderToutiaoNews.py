import os
import requests
import json
import time

START_URL = "https://www.toutiao.com/api/pc/feed/"

GENERY_PARA = {
    "category": "__all__",
    "utm_source": "toutiao",
    "_signature": "XntwuQAABM-Gfiij8tXdmF57cK",
    "as": "A125FA4B05FB3DA&cp=5AB57BD36D3ADE1",
    "max_behot_time": 0,
    "max_behot_time_tmp": 0,
    "widen": 1
}
if __name__ == "__main__":
    aCookie = {"cookie": '''
        uuid="w:5ffa14ae296f40f08229d3919c9a9730"; csrftoken=507bfea64d9314c23137a01b80e088fb; __utma=24953151.568239780.1499689176.1504956717.1504956717.1; uid_tt=0458becd862daec85c1fa9c16b09110d; _ba=BA0.2-20170715-51d9e-buvNklGp4n4PJ9h4DmPW; tt_webid=6441115964263679502; WEATHER_CITY=%E5%8C%97%E4%BA%AC; _ga=GA1.2.568239780.1499689176; tt_webid=6441115964263679502; UM_distinctid=160e54f3a82908-01c19ffad22fe2-32607402-13c680-160e54f3a839e8; odin_tt=e0c14af03526d18eb4fb451ef78f230f3b0c1fa374fb29ff92160302bb0783ea9540c0ffe87e43405b1ce929c81dfc24; utm_source=toutiao; tt_track_id=fda9fa9c847a29067d8638880d04cbba; sso_login_status=0; login_flag=2f9f867b92bd3f46cc671bed03561c83; sessionid=2e37a104242cb6694be0a8e0fd3e1583; sid_tt=2e37a104242cb6694be0a8e0fd3e1583; sid_guard="2e37a104242cb6694be0a8e0fd3e1583|1521618585|15552000|Mon\054 17-Sep-2018 07:49:45 GMT"; _gid=GA1.2.936302519.1521712193; CNZZDATA1259612802=1561649699-1499685480-%7C1521794725; __tasessionId=vmd0pz7ss1521857497574
        '''.strip()}
    aHeader = {
        "cookie": '''
        uuid="w:5ffa14ae296f40f08229d3919c9a9730"; csrftoken=507bfea64d9314c23137a01b80e088fb; __utma=24953151.568239780.1499689176.1504956717.1504956717.1; uid_tt=0458becd862daec85c1fa9c16b09110d; _ba=BA0.2-20170715-51d9e-buvNklGp4n4PJ9h4DmPW; tt_webid=6441115964263679502; WEATHER_CITY=%E5%8C%97%E4%BA%AC; _ga=GA1.2.568239780.1499689176; tt_webid=6441115964263679502; UM_distinctid=160e54f3a82908-01c19ffad22fe2-32607402-13c680-160e54f3a839e8; odin_tt=e0c14af03526d18eb4fb451ef78f230f3b0c1fa374fb29ff92160302bb0783ea9540c0ffe87e43405b1ce929c81dfc24; utm_source=toutiao; tt_track_id=fda9fa9c847a29067d8638880d04cbba; sso_login_status=0; login_flag=2f9f867b92bd3f46cc671bed03561c83; sessionid=2e37a104242cb6694be0a8e0fd3e1583; sid_tt=2e37a104242cb6694be0a8e0fd3e1583; sid_guard="2e37a104242cb6694be0a8e0fd3e1583|1521618585|15552000|Mon\054 17-Sep-2018 07:49:45 GMT"; _gid=GA1.2.936302519.1521712193; __tasessionId=ccifqs4p81521859371997; CNZZDATA1259612802=1561649699-1499685480-%7C1521859526
        '''.strip(),
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }
    aRes = requests.get(START_URL, headers=aHeader, params=GENERY_PARA)
    aData = json.loads(aRes.text)
    print("init url is " + aRes.url)
    while "success" == aData["message"]:
        nextToken = aData["next"]
        if nextToken:
            maxHotTime = nextToken["max_behot_time"]
            GENERY_PARA["max_behot_time"] = maxHotTime;
            GENERY_PARA["max_behot_time_tmp"] = maxHotTime;
            res = requests.get(START_URL, params=GENERY_PARA, headers=aHeader)
            print("the max_behot time is %s,request url is %s" % (maxHotTime, res.url))
            aData = res.json()
            print(res.json())
