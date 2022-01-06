import scrapy
from JOBTOP10.items import Jobtop10Item  # 导入Item类
from JOBTOP10.middlewares import Jobtop10DownloaderMiddleware  # 导入下载中间件类
import time
from datetime import datetime
from selenium import webdriver
from scrapy import signals
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import json
class UESTCJOBSpider(scrapy.spiders.Spider):
    name = "UESTCJOB"  # 定义爬虫的名字
    allowed_domains = [
        "yjsjob.uestc.edu.cn"]  # 描述网站域名
    start_urls = [
        "https://yjsjob.uestc.edu.cn/coread/listeminfo.action?page=1"]
    #json:https://yjsjob.uestc.edu.cn/coread/listeminfo.action?page=1
    #ui:https://yjsjob.uestc.edu.cn/coread/more-eminfo.jsp
    
    pagenum = 1

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     # spider = super(XDUJOBSpider, cls).from_crawler(
    #     #     crawler, *args, **kwargs)
    #     # # 创建 浏览器
    #     # spider.driver = webdriver.Firefox()
    #     # crawler.signals.connect(spider.spider_closed,
    #     #                         signal=signals.spider_closed)
    #     # return spider
    #     pass
    # def spider_closed(self, spider):
    #     # spider.driver.close()  # 关闭浏览器
    #     print("==========爬虫结束！==========")
    #     spider.logger.info('Spider closed:%s', spider.name)

    def start_requests(self):
        yield scrapy.Request('https://yjsjob.uestc.edu.cn/coread/listeminfo.action?page=1',
                             callback=self.parse, meta={'method': "stastic"})
    def parse(self, response):  # 解析爬取的内容
        data = json.loads(response.body)   # 获取网页的json数据
        jobpost_list = data['list']
        print("[UESTC]now pagenum:"+str(data['page']))
        print("[UESTC]job len:"+str(len(jobpost_list)))
        for jobpost in jobpost_list:
            jobtime=jobpost["date"]
            jobtime = jobtime.replace("年", '-').replace("月", '-').replace("日", '')
            # print(jobtime)
            if datetime.strptime(jobtime, '%Y-%m-%d') < datetime.strptime('2021-09-01', '%Y-%m-%d'):
                return None
            item = Jobtop10Item()
            item['job_title'] = jobpost['title']
            item['job_date'] = jobtime
            item['job_views'] = jobpost['viewcount']
            item['job_nums'] = 1
            yield item
        self.n = data['page']+1
        if self.n <= data['totalPage']:
            yield scrapy.Request(url='https://yjsjob.uestc.edu.cn/coread/listeminfo.action?page={}'.format(self.n),
                                     callback=self.parse, meta={'method': "stastic"})
        
        
