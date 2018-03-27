import pymysql
import time
import sys
import os

moDir="/home/ubuntu/spider/mySpider"
sys.path.append(moDir)
from first.first.mails.sendMail import sendNotifiedMessage

notiGap = 1 * 60 * 60;
testNoti = 3;
if __name__ == "__main__":
    # 用来通知数据库新闻数量的
    if len(sys.argv) >= 2:
        if sys.argv[1].isdigit():
            print("设置通知时间间隔为 {0} 小时".format(sys.argv[1]))
            notiGap = int(sys.argv[1]) * 60 * 60;

    sendTimes = 0
    while True:
        try:
            con = pymysql.connect(host="localhost", user="ldy", password="abcd1234",
                          database="spider", charset="utf8")
            cursor = con.cursor()
            exSql = '''
                select count(*) from toutiao_news;
            '''
            cursor.execute(exSql)
            result = cursor.fetchone()
            number = result[0];
            hours=time.strftime("%H",time.localtime())
            # print("hours is {0}".format(hours))
            if int(hours)>=23 or int(hours)<=9:
              continue;
            print("开始发送邮件...{0},新闻数量为{1}".format(sendTimes,number))
            sendNotifiedMessage("云服务器,现在新闻数量为 {0}，发送次数为 {1}".format(number, sendTimes), "新闻数据库数量")
            sendTimes = sendTimes + 1
            time.sleep(notiGap)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            con.close()
