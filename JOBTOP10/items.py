# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Jobtop10Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()  # 招聘帖子的主题
    job_date  = scrapy.Field()  # 招聘帖子的发帖时间
    job_views = scrapy.Field()  # 招聘帖子的浏览次数
    job_nums  = scrapy.Field()  # 招聘帖子的职位数量