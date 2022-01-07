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
class BUPTJOBSpider(scrapy.spiders.Spider):
    name="BUPTJOB"
    allowed_domains = ["job.bupt.edu.cn"]
    # start_urls = ['https://job.bupt.edu.cn/f/recruitmentinfo/ajax_frontRecruitinfo?pageNo=']
    pagenum=1
    def start_requests(self):
        #由于start_urls不能传静态爬取参数，用start_requests
        yield scrapy.Request('https://job.bupt.edu.cn/f/recruitmentinfo/ajax_frontRecruitinfo?pageNo=',
                             callback=self.parse, meta={'method': "stastic"})
    def parse(self, response):
        data = json.loads(response.body)   
        # 获取网页的json数据
        jobpost_list = data['object']['list']
        print("[BUPT]now pagenum:"+str(data['object']['pageNo']))
        print("[BUPT]job len:"+str(len(jobpost_list)))
        for jobpost in jobpost_list:
            if datetime.strptime(jobpost["startTime"], '%Y-%m-%d %H:%M:%S') < datetime.strptime('2021-09-01', '%Y-%m-%d'):
                break
            id = jobpost['id']
            #获取下一页url，到二级页面爬取
            yield scrapy.Request(url=f'https://job.bupt.edu.cn/f/recruitmentinfo/ajax_show?recruitmentId={id}', 
                                 callback=self.parse_details, meta={'method': "stastic"})#回调函数改变
        self.n=data['object']['pageNo']+1
        if not data['object']['lastPage']:
            #判断尾页
            yield scrapy.Request(url=f'https://job.bupt.edu.cn/f/recruitmentinfo/ajax_frontRecruitinfo?pageNo={self.n}', 
                                    callback=self.parse, meta={'method': "stastic"})
    def parse_details(self, response):
        #爬详情页，代码非常简单
        item = Jobtop10Item()
        data = json.loads(response.body)
        job = data['object']['recruitmentinfo']
        item['job_title'] = job['title']
        item['job_date'] = job['startTime']
        item['job_views'] = job['browseNumber']
        item['job_nums'] = job['positionNum']
        yield item
