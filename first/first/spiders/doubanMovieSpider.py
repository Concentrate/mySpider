import scrapy
from ..items import FirstItem,DoubanItem


class doubanSpider(scrapy.Spider):
    name = "doubanSpider"
    start_urls = ["https://movie.douban.com/cinema/nowplaying/langfang/"]
    allow_domains = ["douban.com"]

    def parse(self, response):
        aSelector = scrapy.Selector(response=response)
        ulDiv = aSelector.xpath('//ul[@class="lists"]/li/ul');
        for node in ulDiv:
            try:
                item = DoubanItem()
                item['name'] = node.xpath('./li[@class="stitle"]/a/@title').extract_first()
                item["picture"] = node.xpath('./li[@class="poster"]/a/img/@src').extract_first()
                item["grade"] = node.xpath('./li[@class="srating"]/span[@class="subject-rate"]/text()').extract_first()
                yield item
            except Exception as e:
                print(e)
