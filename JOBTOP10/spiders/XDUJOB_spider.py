import scrapy
from JOBTOP10.items import Jobtop10Item  # 导入Item类
from JOBTOP10.middlewares import Jobtop10DownloaderMiddleware  # 导入下载中间件类
import time
from datetime import datetime
from selenium import webdriver
from scrapy import signals
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

##爬到十八页
class XDUJOBSpider(scrapy.spiders.Spider):
    name = "XDUJOB"  # 爬虫的名字
    allowed_domains = ["job.xidian.edu.cn"]#允许访问的网站域名
    start_urls = ["https://job.xidian.edu.cn/campus/index?domain=xidian&city=&page=1"]
    #起始页
    xidian_next_page=''
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(XDUJOBSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        # 创建浏览器
        spider.driver = webdriver.Firefox()
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider
    def spider_closed(self, spider):
        spider.driver.close()  # 关闭浏览器
        print("==========爬虫结束！==========")
        spider.logger.info('Spider closed:%s', spider.name)

    def parse(self, response): #解析爬取的内容
        item = Jobtop10Item()
        #下一页的url
        next_page_href = response.css('li[class="next"]>a::attr(href)').extract()
        # 末尾页的url
        last_page_href = response.css('li[class="last"]>a::attr(href)').extract()
        #确认现在页面不是最后一页
        #在尾页页的时候页面发生改变，尾页的链接在li[class="last "]下
        #按上面代码无法获取，由于只有一页，直接用len判断
        if response.url != last_page_href and len( last_page_href) :
            self.xidian_next_page = 'https://job.xidian.edu.cn' + next_page_href[0]
        else:
            self.xidian_next_page = ''   
        c_page_url_list = response.css('ul[class="infoList"]>li:nth-child(1)>a')
        for job in c_page_url_list:  # 循环打开和解析每个详情页
            driver=self.driver #用爬虫定义的driver
            driver.get('https://job.xidian.edu.cn' + job.css('a::attr(href)').extract()[0])
            time.sleep(2)#等待2秒钟
            item['job_title'] = [driver.find_element(
                'css selector', 'div[class="title-message"]>h5').text][0]
            date_text = driver.find_element('css selector', 'div[class="share"]>ul>li:nth-child(1)').text
            date_text=date_text[date_text.find('：') + 1:] 
            if datetime.strptime(date_text,'%Y-%m-%d %H:%M')<datetime.strptime('2021-09-01 00:00','%Y-%m-%d %H:%M'):
                self.xidian_next_page=''
                #到了设定时间，停止爬取。刚好可以利用下一页的url作为结束标志
                break
            item['job_date'] = [date_text][0] 
            views_text = driver.find_element('css selector', 'div[class="share"]>ul>li:nth-child(2)').text
            item['job_views'] = [views_text[views_text.find('：') + 1:]][0]  
            item['job_nums']=1
            yield item
        #处理完列表页的所有二级页面后，继续打开下一页进行抓取
        if self.xidian_next_page!='':
        #如果没有下一页了，停止爬取
            yield scrapy.Request(self.xidian_next_page, callback=self.parse)
