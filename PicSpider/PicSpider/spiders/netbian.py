import scrapy
from scrapy.http import Request
from urllib import parse,request
from ..items import ImageItem



class NetbianSpider(scrapy.Spider):
    name = "netbian"
    allowed_domains = ["pic.netbian.com"]
    start_urls = ["https://pic.netbian.com"]

    def parse(self, response):
        pass
        '''
        返回分页url给下一个函数处理
        :param response:
        :return:
        '''       

        #获取下一页的url
        next_page_url = response.xpath('//div[@class="page"]/a[contains(text(),"下一页")]/@href').extract()[0]
        next_url = parse.urljoin(self.start_urls[0],next_page_url)

        yield Request(response.url,
                      meta={'next_url': next_url},
                      callback=self.page_parse,
                      )


    def page_parse(self,response):
        '''
        根据当前分页，获取图片详情页的url
        :param response:
        :return:
        '''
        # 获取图片详情页的html元素信息列表
        img_list = response.xpath('//ul[@class="clearfix"]/li/a/@href').extract()
        next_url = response.meta['next_url']
        # print('next_url:'+next_url)
        for url in img_list:
            img_html_url = parse.urljoin(self.start_urls[0],url)
            # print(img_html_url)
            yield Request(img_html_url,callback=self.img_url_parse,dont_filter=True)

        yield Request(next_url,callback=self.parse,dont_filter=True)


    def img_url_parse(self,response):
        '''
        进入图片详情页，爬取大图url
        获取标题
        :param response:
        :return:
        '''
        # 实例化item对象
        item = ImageItem()

        img_big_url = response.xpath('//div[@class="photo-pic"]/a/img/@src').extract()[0]
        img_title = response.xpath('//div[@class="photo-pic"]/a/img/@alt').extract()[0].strip()

        img_category = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/p[1]/span/a/text()').extract_first()
        if img_category == None:
            img_category = response.xpath(' //*[@id="main"]/div[2]/div[2]/div[3]/p[1]/span/a/text()').extract_first()
        img_time = response.xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/p[4]/span/text()').extract_first()
        if img_time == None:
             img_time = response.xpath('//*[@id="main"]/div[2]/div[2]/div[3]/p[4]/span/text()').extract_first()
        img_url = parse.urljoin(self.start_urls[0],img_big_url)
        img_source = request.urlopen(img_url).read() #二进制


        item['url'] = img_url    # 设置图片来源，如果有的话
        item['title'] = img_title
        item['source'] =  img_source     # 保存图片
        item['is_public'] = True
        item['category'] = img_category  # 设置图片分类，如果有的话
        item['crawl_time'] =  img_time  # 设置爬取时间

        yield item
