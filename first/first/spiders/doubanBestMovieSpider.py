import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from ..items import DoubanItem


class BestMovieSpider(CrawlSpider):
    name = "BestMovieSpider"
    start_urls = ["https://www.douban.com/doulist/240962/"]
    allow_domains = ["douban.com"]
    rules = (
        Rule(LinkExtractor(allow=(r'/doulist/\d+/.*start=\d+&sort=seq&sub_type=')), callback="item_parse_callback",
             follow=True),
    )

    def item_parse_callback(self, response):
        divs = response.xpath("//div[contains(@id,'item')]")
        if not divs:
            return
        for aNode in divs:
            if not aNode:
                continue
            item = DoubanItem()
            try:
                item["picture"] = aNode.xpath('.//div[@class="post"]/a/img/@src').extract_first()
                item["name"] = aNode.xpath('.//div[@class="title"]/a/text()').extract_first()
                item["grade"] = aNode.xpath(
                    './/div[@class="rating"]/span[@class="rating_nums"]/text()').extract_first()
                item["gradeNum"] = aNode.xpath('.//div[@class="rating"]/span/text()').re(r'\((.*)\)')
                item["file_urls"]=[item["picture"],]
                yield item
            except Exception as e:
                print(e)
