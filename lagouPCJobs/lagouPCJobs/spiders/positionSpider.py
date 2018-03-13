import scrapy
from lagouPCJobs.items import LagoupcjobsItem
from scrapy import Selector
from urllib import parse


class PositionSpider(scrapy.Spider):
    name = 'position'

    def __init__(self):
        super(PositionSpider, self).__init__()
        self.position_name = 'Python'
        self.city = parse.urlencode({'city': '全国'})
        self.start_urls = [
            'https://www.lagou.com/jobs/list_%s?%s' % (self.position_name, self.city)
        ]

    def parse(self, response):
        while True:
            if response.body == 'Finish':
                break
            content = response.body.decode('utf-8')
            for i in range(1, 16):
                item = LagoupcjobsItem()
                item['positionName'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[1]/div[1]/a/h3/text()' % str(i)).extract_first()
                item['location'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[1]/div[1]/a/span/em/text()' % str(i)).extract_first()
                item['salary'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[1]/div[2]/div/span/text()' % str(i)).extract_first()
                item['experience'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[1]/div[2]/div/text()' % str(i)).extract()
                item['company'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[2]/div[1]/a/text()' % str(i)).extract_first()
                item['type'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[2]/div[2]/text()' % str(i)).extract_first()
                item['description'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[2]/div[2]/text()' % str(i)).extract_first()
                item['tag'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[2]/div[1]/span/text()' % str(i)).extract()
                item['site'] = Selector(text=content).xpath(
                    '//*[@id="s_position_list"]/ul/li[%s]/div[1]/div[1]/div[1]/a/@href' % str(i)).extract_first()
                yield item
            yield scrapy.Request(response.url, dont_filter=True)
        print('')
