# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanItem(scrapy.Item):
    name = scrapy.Field()
    picture = scrapy.Field()
    grade = scrapy.Field()
    gradeNum = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

    def executeSql(self, con, aCursor):
        aSql = '''
        insert into douban(name,picUrl,grade,totalNum) VALUES (%s,%s,%s,%s)
        '''
        res = aCursor.execute(aSql, (
        str(self.get("name")), str(self.get("picture")), str(self.get("grade")), str(self.get("gradeNum"))))
        print("execute sql res is " + str(res))
        con.commit()
