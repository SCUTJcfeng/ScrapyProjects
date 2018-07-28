# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import requests
import execjs
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from wenshu.settings import USER_AGENTS
from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware


class WenshuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WenshuDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        with open('./wenshu/js/process.js', 'r') as f:
            default = execjs.get('phantomjs')
            data = f.read()
            ect = default.compile(data)
            guid = ect.call('getGuid')
            number = self.get_code(guid)
            vjkl5 = self.get_vjkl5()
            vl5x = ect.call('getKey', vjkl5)
            headers = (
                {
                    'user-agent': random.choice(USER_AGENTS),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            )
            cookies = {
                'vjkl5': vjkl5
            }
            data = {
                'Param': request.meta['Param'],
                'Index': request.meta['Index'],
                'Page': request.meta['Page'],
                'Order': request.meta['Order'],
                'Direction': request.meta['Direction'],
                'vl5x': vl5x,
                'number': number,
                'guid': guid
            }
            res = requests.post(request.url, data=data, headers=headers, cookies=cookies)
            return HtmlResponse(request.url, body=res.text, encoding='utf8')

    def get_code(self, guid):
        url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
        s = requests.Session()
        s.headers.update(
            {
                'user-agent': random.choice(USER_AGENTS),
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        )
        data = {
            'guid': guid
        }
        res = s.post(url, data=data)
        return res.text

    def get_vjkl5(self):
        url = 'http://wenshu.court.gov.cn/list/list/?sorttype=1'
        headers = (
            {
                'user-agent': random.choice(USER_AGENTS),
            }
        )
        res = requests.get(url, headers=headers)
        return res.cookies['vjkl5']

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class WenshuUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=random.choice(USER_AGENTS)):
        super().__init__(user_agent)

class WenshuHeadersMiddleware(DefaultHeadersMiddleware):
    def __init__(self, headers=({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})):
        super().__init__(headers)

class WenshuCookiesMiddleware(CookiesMiddleware):
    def __init__(self):
        super().__init__()
