import scrapy
from urllib import parse
import json
from lagouJobs import items


class PositionSpider(scrapy.Spider):
    name = 'position'
    positionName = 'python'
    pageNo = 1
    city = parse.urlencode({'city': '全国'})
    start_urls = [
        'http://m.lagou.com/search.json?%s&positionName=%s&pageNo=%d&pageSize=15'
        % (city, positionName, pageNo)
    ]

    def parse(self, response):
        jsonbody = json.loads(response.body)
        jsoncontent = jsonbody['content']
        jsondata = jsoncontent['data']
        jsonpage = jsondata['page']
        results = jsonpage['result']
        item = items.LagoujobsItem()
        for result in results:
            item['city'] = result['city']
            item['companyName'] = result['companyName']
            item['companyId'] = result['companyId']
            item['positionName'] = result['positionName']
            item['positionId'] = result['positionId']
            item['salary'] = result['salary']
            item['companyFullName'] = result['companyFullName']
            yield item
        self.pageNo += 1
        next_url = 'http://m.lagou.com/search.json?%s&positionName=%s&pageNo=%d&pageSize=15'\
                   % (self.city, self.positionName, self.pageNo)
        yield scrapy.Request(next_url)
