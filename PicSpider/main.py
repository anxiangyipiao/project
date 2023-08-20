from scrapy.cmdline import execute
import sys
import os

# #这里就不细说了，反正命令行的命令都用这个叫execute的函数来执行就完事了，
# #命令用列表存放
# #每次运行这个文件就行了
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# #execute(["scrapy","crawl","netbian"])
# execute(["scrapy","crawl","novel"])
# #scrapy crawl netbian

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 定义要运行的爬虫名称列表
spiders = ["netbian", "novel"]

# 获取 Scrapy 项目的设置
settings = get_project_settings()

# 创建 CrawlerProcess 实例
process = CrawlerProcess(settings)

# 并行运行多个爬虫
for spider_name in spiders:
    process.crawl(spider_name)

# 启动爬虫
process.start()
