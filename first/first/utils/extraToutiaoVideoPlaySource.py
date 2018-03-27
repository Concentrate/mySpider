# 抽取数据库里面视频资源脚本，并存进另一个数据库里面
import you_get
import pymysql
import json
from functools import reduce
import os
import time

localUser, yunUser = "ldy", "ubuntu"
db = pymysql.connect(user=localUser, password="abcd1234", database="spider", charset="utf8")


def create_table():
    create_Video_Table = '''
    create table if not EXISTS toutiao_video_source(video_id varchar(200) not null,
    container varchar(30),
    size long,
    src varchar(400),
    behot_time long,
    title varchar(400),
    video_site varchar(100)
    ) default charset="utf8";
    '''
    cursor = db.cursor()
    res = cursor.execute(create_Video_Table)
    print("execute result is {0}".format(res))
    cursor.close()
    db.commit()


def dealWithInserVideoSource(video_id, source_url, be_hottime):
    cursor = db.cursor()
    find_one_video_sql = '''
    select video_id from toutiao_video_source where video_id="{0}"
    '''.format(video_id)
    insert_into_video_table = '''
    insert into toutiao_video_source(video_id,container,size,src,behot_time,title,video_site) VALUES("{0}","{1}","{2}","{3}","{4}","{5}","{6}"); 
    '''
    print("find sql is {0}".format(find_one_video_sql))
    cursor.execute(find_one_video_sql)
    find_res = cursor.fetchone()
    if find_res:
        print(find_res)
        return False;
    else:
        print("execute extral video url ,and source url is {0}".format(source_url))
        ex_you_get_cmd = '''
        you-get {0} --json
        '''.format(source_url)
        try:
            cmd_res_list = os.popen(ex_you_get_cmd).readlines()
            real_output_res_str = ""
            real_output_res_str = reduce(lambda a, b: a + b, cmd_res_list)
            aJson = json.loads(real_output_res_str)
            print("the json is " + str(aJson))
            title = aJson.get("title")
            video_site = aJson.get("site")
            streamLoader = aJson.get("streams")
            if streamLoader:
                streamLoader = streamLoader.get("__default__")
                contianer = streamLoader.get("container")
                size = streamLoader.get("size")
                src = streamLoader.get("src")[0]
            inser_sql = insert_into_video_table.format(video_id, contianer, size, src, be_hottime, title, video_site)
            print("insert sql is {0}".format(inser_sql))
            insert_video_sql_res = cursor.execute(inser_sql)
            print("execute insert video source result is {0}".format(insert_video_sql_res))
            db.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        return True


def extraVideoSource():
    find_video_sql = '''
    select video_id,source_url,behot_time from toutiao_news where video_id!=0 ORDER by behot_time desc;
    '''
    cursor = db.cursor()
    cursor.execute(find_video_sql)
    all_result = cursor.fetchall()
    if all_result:
        for a1 in all_result:
            video_id = a1[0]
            source_url = a1[1]
            be_hottime = a1[2]
            if not dealWithInserVideoSource(video_id, source_url, be_hottime):
                break


if __name__ == "__main__":
    create_table()
    while True:
        try:
            extraVideoSource()
            print("休眠15分钟，已无新的资源需要抽取视频资源")
            time.sleep(15 * 60)
        except Exception as e:
            print("something wrong,but continue")
            print(e)
