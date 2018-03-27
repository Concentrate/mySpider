import requests
import math
import time
import hashlib


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


if __name__ == "__main__":
    tmp_header = {
        "cookie": '''
      tt_webid	=6536062094340802052		
      '''.strip()
    }
    while True:
        a1, a2 = getASCP()
        response = requests.get(get_url(0, a1, a2), headers=tmp_header)
        print(response.json())
