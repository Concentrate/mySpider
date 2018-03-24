# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from .items import DoubanItem
import pymysql

class FirstPipeline(object):
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        pass


class JsonPipeLine(object):
    def __init__(self):
        self.file = open("resultjson.json", "w", encoding="utf8");
        self.jArray = []

    def process_item(self, item, spider):
        self.jArray.append(dict(item))
        # line = json.dumps(dict(item), ensure_ascii=False)
        # self.file.write(line + "\n")
        # self.file.flush()
        return item

    def close_spider(self, spider):
        self.file.write(json.dumps(self.jArray, ensure_ascii=False))
        self.file.flush()
        self.file.close()


class MySqlPipeLine(FirstPipeline):

    def __init__(self):
        self.con=pymysql.connect(user="ldy",password="abcd1234",db="spider",charset="utf8")
        self.cursor=self.con.cursor()

    def process_item(self, item, spider):
        if type(item) is DoubanItem:
            DoubanItem(item).executeSql(self.con,self.cursor)
        return item

    def close_spider(self, spider):
        self.con.close()
        self.cursor.close()
        super().close_spider(spider)
