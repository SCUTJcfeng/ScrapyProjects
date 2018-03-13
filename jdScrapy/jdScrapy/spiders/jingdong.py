from scrapy import Spider
import scrapy
from jdScrapy.items import JdscrapyItem
from scrapy import Selector


class jingdongspider(scrapy.Spider):
    name = 'jd'

    def __init__(self):
        super().__init__()
        self.start_urls = [
            'https://list.jd.com/list.html?cat=670,677,679'  # 3个数字分别指代电脑办公、电脑配件、显卡3大分类
        ]

    def clean_data(self, data):
        data = data.replace('\n', '')
        return data.strip()

    def parse(self, response):
        while True:
            body = response.body.decode('utf-8')
            if body == 'Finish':
                break
            for i in range(1, 61):
                item = JdscrapyItem()
                item['title'] = Selector(text=body).xpath('//*[@id="plist"]/ul/li[%d]/div/div[3]/a/em/text()' % i).extract_first()
                item['description'] = Selector(text=body).xpath('//*[@id="plist"]/ul/li[%d]/div/div[3]/a/i/text()' % i).extract_first()
                item['comment'] = Selector(text=body).xpath('//*[@id="plist"]/ul/li[%d]/div/div[4]/strong/a/text()' % i).extract_first()
                item['shop'] = Selector(text=body).xpath('//*[@id="plist"]/ul/li[%d]/div/div[5]/span/a/text()' % i).extract_first()
                item['price'] = Selector(text=body).xpath('//*[@id="plist"]/ul/li[%d]/div/div[2]/strong[1]/i/text()' % i).extract_first()
                item['id'] = Selector(text=body).xpath('//*[@id="plist"]/ul/li[%d]/div/@data-sku' % i).extract_first()
                try:
                    item['title'] = self.clean_data(item['title']) # 有的只有title没有shop，奇葩了，位置有顺序要求
                    item['shop'] = self.clean_data(item['shop'])
                except AttributeError as e: # 因为这款产品有套装，XPath变了，这边跳过不抓
                    pass
                yield item
            yield scrapy.Request(response.url)
