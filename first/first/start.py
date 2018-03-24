from scrapy import cmdline
import os
import subprocess

if __name__ == "__main__":
    str = 'scrapy crawl BestMovieSpider';
    changeDir = "/Users/liudeyu/IdeaProjects/spiderPratise/first";
    os.chdir(changeDir)
    os.system(str)