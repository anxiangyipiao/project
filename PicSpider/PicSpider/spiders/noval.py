import scrapy
from ..items import NovelItem  # 替换为实际的项目路径和导入方式
from urllib import parse,request
from scrapy.http import Request


class NovelSpider(scrapy.Spider):
    name = "novel"
    allowed_domains = ["www.qisuwang.cc"]  # 替换为小说网站的域名
    start_urls = ["https://www.qisuwang.cc/all/"]  # 替换为小说列表页的URL
    start_url = 'https://www.qisuwang.cc'
    def parse(self, response):
        
        # 解析小说列表页，获取每本小说的详情页URL
        next_page_url = response.xpath('//*[@id="splitpage"]/ul/li[11]/a/@href').extract()[0]
        next_url = parse.urljoin(self.start_url,next_page_url)

        yield Request(response.url,
                      meta={'next_url': next_url},
                      callback=self.page_parse,
                      )


    def page_parse(self,response):

        # 获取图片详情页的html元素信息列表
        book_list = response.xpath('//div[@class="pic"]/a/@href').extract()
        
        next_url = response.meta['next_url']

        for url in book_list:
            img_html_url = parse.urljoin(self.start_url,url)
           
            yield Request(img_html_url,callback=self.parse_novel,dont_filter=True)

        yield Request(next_url,callback=self.parse,dont_filter=True)


    def parse_novel(self, response):
        
        item = NovelItem()
        
        # 获取小说标题、作者、内容等信息  
        title = response.xpath('//dd[@class="bt"]/h2/text()').extract_first()
        author = response.xpath('(//dd[@class="db"]/a/text())[1]').extract_first()
        category = response.xpath('(//dd[@class="db"][3]/a/text())').extract_first()
        crawl_time = response.xpath('(//dd[@class="db"][7]/span/text())').extract_first()
        size = response.xpath('(//dd[@class="db"][6]/span/text())').extract_first()
        img_url = response.xpath('//img[@class="pics3"]/@src').extract_first()
        des_content = response.xpath('(//div[@class="cont"]/text())[2]').extract()

        item['title'] = title
        item['size'] = size
        item['url'] = img_url
        item['des'] = des_content
        item['author'] = author
        item['category'] = category  # 设置小说分类，如果有的话
        item['is_public'] = True
        item['crawl_time'] = crawl_time  # 设置爬取时间

        content_url = response.xpath('//div[@class="downlinks"]/ul/li/p/b/a/@href').extract_first()
        content_url = parse.urljoin(self.start_url,content_url)


        yield scrapy.Request(content_url, callback=self.parse_content, meta={'item': item})

    def parse_content(self, response):

        item = response.meta['item']
        download_link = response.xpath('//div[@class="downlist"]/li/strong/a/@href').extract_first()   
        item['content'] =  download_link

        
        yield item
