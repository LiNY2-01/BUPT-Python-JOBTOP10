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
        yield scrapy.Request('https://job.bupt.edu.cn/f/recruitmentinfo/ajax_frontRecruitinfo?pageNo=',
                             callback=self.parse, meta={'method': "stastic"})
   
    def parse(self, response):
        data = json.loads(response.body)   # 获取网页的json数据
        jobpost_list = data['object']['list']
        print("now pagenum:"+str(data['object']['pageNo']))
        print("job len:"+str(len(jobpost_list)))
        for jobpost in jobpost_list:

            if datetime.strptime(jobpost["startTime"], '%Y-%m-%d %H:%M:%S') < datetime.strptime('2021-12-21', '%Y-%m-%d'):
                break
            id = jobpost['id']
            yield scrapy.Request(url=f'https://job.bupt.edu.cn/f/recruitmentinfo/ajax_show?recruitmentId={id}', 
                                 callback=self.parse_details, meta={'method': "stastic"})
        else:
            self.n=data['object']['pageNo']+1
            if not data['object']['lastPage']:
                yield scrapy.Request(url=f'https://job.bupt.edu.cn/f/recruitmentinfo/ajax_frontRecruitinfo?pageNo={self.n}', 
                                     callback=self.parse, meta={'method': "stastic"})
        
    def parse_details(self, response):
        item = Jobtop10Item()
        data = json.loads(response.body)
        job = data['object']['recruitmentinfo']
        item['job_title'] = job['title']
        item['job_date'] = job['startTime']
        item['job_views'] = job['browseNumber']
        item['job_nums'] = job['positionNum']
        
        yield item
