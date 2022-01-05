from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError

class Command(BaseRunSpiderCommand):
    requires_project = True
    def syntax(self):
        return "[options] <spider>"
    def short_desc(self):
        return "Run multiple spiders"
    def run(self, args, opts):
        # 获取爬虫列表
        spd_loader_list = self.crawler_process.spider_loader.list()
        # 遍历各爬虫
        for spname in spd_loader_list or args:
            self.crawler_process.crawl(spname, **opts.spargs)
            print("##############此时启动的爬虫##############：" + spname)
        self.crawler_process.start()
