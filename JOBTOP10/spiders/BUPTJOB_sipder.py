import scrapy
from JOBTOP10.items import Jobtop10Item  # 导入Item类
from JOBTOP10.middlewares import Jobtop10DownloaderMiddleware  # 导入下载中间件类
import time
from datetime import datetime
from selenium import webdriver
from scrapy import signals
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
class BUPTJOBSpider(scrapy.spiders.Spider):
    name="BUPTJOB"
    allowed_domains = ["https://job.bupt.edu.cn"]
    start_urls = [
        "https://job.bupt.edu.cn/frontpage/bupt/html/recruitmentinfoList.html?type=1"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BUPTJOBSpider, cls).from_crawler(crawler, *args, **kwargs)
        # 创建 浏览器
        spider.driver = webdriver.Firefox()
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.driver.close()  # 关闭浏览器
        print("==========爬虫结束！==========")
        spider.logger.info('Spider closed:%s', spider.name)

    def check_lastpage(response):
        if response(".fPage>li:last-child>a::attr(href)").extract() is None:
            return False
        else :
            return True
    def parse(self, response):
        spiderflag = 1
        driver = self.driver
        while spiderflag:            
            
            nxtbtn=driver.find_element("css selector", ".fPage>li:last-child>a")
            nxtbtn_herf = nxtbtn.get_attribute("href")
            if nxtbtn_herf is None:
                print("BUPT last page got!")
                spiderflag = 0
                # d = nxtbtn.execute_script('return arguments[0].click();', e)
    
            jobpost_div_list = driver.find_elements("css selector",
                'div[class="infoItem collected recmmonded"]>div[class="left"]')
            for jobpost in jobpost_div_list:
                jobpost_link = jobpost.find_element(
                    "css selector", 'a[class="tit"]').get_attribute("href")
                print(jobpost_link)
                jobpost_date = jobpost.find_element("css selector",'span[class="time"]').text
                te = datetime.strptime(jobpost_date, '%Y-%m-%d')
                if datetime.strptime(jobpost_date, '%Y-%m-%d') < datetime.strptime('2021-12-29', '%Y-%m-%d'):
                    spiderflag = 0
                    break  # 测试时候设定时间为'2021-12-01'，正式执行时候，此处时间按要求设置为'2021-09-01'
                # driver.get(job.css('a[class="tit"]::attr(href)').extract()[0])
            driver.execute_script('return arguments[0].click();', nxtbtn)
            time.sleep(3)

    def parse_details(self, response):
        #pass
        item = Jobtop10Item()
        print(response.url)
