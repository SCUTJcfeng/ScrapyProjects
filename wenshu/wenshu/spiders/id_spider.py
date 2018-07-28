from scrapy import Spider
import scrapy
import json
from time import sleep
from wenshu.items import WenshuItem


class IdSpider(Spider):
    name = 'id'

    def __init__(self):
        super().__init__()
        self.url = 'http://wenshu.court.gov.cn/List/ListContent'
        self.param = ''
        self.index = 36
        self.page = 20
        self.order = '法院层级'
        self.direction = 'asc'

    def start_requests(self):
        meta = {
                'Param': self.param,
                'Index': self.index,
                'Page': self.page,
                'Order': self.order,
                'Direction': self.direction,
                'vl5x': None,
                'number': None,
                'guid': None
        }
        yield scrapy.Request(self.url, method='POST', dont_filter=True, meta=meta)

    def parse(self, response):
        text = response.text.replace('\\', '')
        text = text.lstrip('\"')
        text = text.rstrip('\"')
        data = json.loads(text)
        if data != '':
            del data[0]
            for case in data:
                item = WenshuItem()
                try:
                    item['content'] = case['裁判要旨段原文']
                except:
                    item['content'] = ''
                item['type'] = case['案件类型']
                try:
                    item['date'] = case['裁判日期']
                except:
                    item['date'] = '1970-01-01'
                item['name'] = case['案件名称']
                item['paperId'] = case['文书ID']
                try:
                    item['procedure'] = case['审判程序']
                except:
                    item['procedure'] = ''
                try:
                    item['anhao'] = case['案号']
                except:
                    item['anhao'] = ''
                item['courtName'] = case['法院名称']
                yield item
        sleep(1)
        meta = {
            'Param': self.param,
            'Index': self.index + 1,
            'Page': self.page,
            'Order': self.order,
            'Direction': self.direction,
            'vl5x': None,
            'number': None,
            'guid': None
        }
        print(self.index)
        yield scrapy.Request(self.url, method='POST', meta=meta)
