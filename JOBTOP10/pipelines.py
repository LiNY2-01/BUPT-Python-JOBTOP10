# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from itemadapter import ItemAdapter


class Jobtop10Pipeline:
    def process_item(self, item, spider):
        try :
            dict_item = dict(item)
            if spider.name=='BUPTJOB':
                self.BUPTJOB_writer.writerow(dict_item)
            elif spider.name=="XDUJOB":
                dict_item.pop('job_nums')
                self.XDUJOB_writer.writerow(dict_item)
            elif spider.name=='UESTCJOB':
                dict_item.pop('job_nums')
                self.UESTCJOB_writer.writerow(dict_item)
        except Exception as err:
            print(err)
    def open_spider(self,spider):
        self.BUPTJOB_file=open('BEIYOU_1.csv','w+',newline='',encoding='GB2312')
        self.BUPTJOB_writer = csv.DictWriter(self.BUPTJOB_file, 
                              fieldnames=["job_title","job_date","job_views","job_nums"])
        self.BUPTJOB_writer.writeheader()
        #create bupt job csv file and write header
        self.XDUJOB_file = open('XIDIAN_1.csv', 'w+',
                                 newline='', encoding='GB2312')
        self.XDUJOB_writer = csv.DictWriter(self.XDUJOB_file,
                            fieldnames=["job_title", "job_date", "job_views"])
        self.XDUJOB_writer.writeheader()
        #create xdu job csv file and write header
        self.UESTCJOB_file = open('XIDIAN_1.csv', 'w+',
                                newline='', encoding='GB2312')
        self.UESTCJOB_writer = csv.DictWriter(self.UESTCJOB_file,
                                            fieldnames=["job_title", "job_date", "job_views"])
        self.UESTCJOB_writer.writeheader()
        #create uestc job csv file and write header

    def close_spider(self, spider):
        self.BUPTJOB_file.close()
        self.XDUJOB_file.close()
        self.UESTCJOB_file.close()


