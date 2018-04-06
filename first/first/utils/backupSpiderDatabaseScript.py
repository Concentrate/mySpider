# -*- coding: utf-8 -*-
import os
import time
import datetime
import pymysql

#为防止意外，自动化备份数据库
auto_time=1*24*60*60;
backup_file="~/backup/backup_spider.sql"
count=1
last_count=20*10000;# 最低备份20万起

def detactIfBackup():
    global last_count
    db=pymysql.connect("localhost","ldy","abcd1234","spider")
    cursor=db.cursor()
    ex_sql=''' select count(*) from toutiao_news;'''
    cursor.execute(ex_sql)
    res=cursor.fetchone()
    is_ok=False
    print(res[0])
    if res[0]>last_count:
        is_ok=True
        last_count=res[0]
    cursor.close()
    db.close()
    return is_ok

if __name__=="__main__":
    while True:
        if not detactIfBackup():
            break
        print("开始备份...")
        ex_cmd="mysqldump -u ldy -pabcd1234 spider >{0}".format(backup_file)
        os.system(ex_cmd)
        print("备份次数{0},时间为{1} ".format(count,datetime.datetime.now()))
        print("备份结束...")
        count=count+1
        time.sleep(auto_time)





