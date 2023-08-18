# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    is_public = scrapy.Field(default=True)  # 是否为公开内容，默认为True
    category = scrapy.Field()  # 分类
    crawl_time = scrapy.Field()  # 爬取时间


class NovelItem(scrapy.Item):
    url = scrapy.Field()
    size = scrapy.Field()
    title = scrapy.Field()
    des = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()  # 分类
    is_public = scrapy.Field(default=True)  # 是否为公开内容，默认为True
    crawl_time = scrapy.Field()  # 爬取时间