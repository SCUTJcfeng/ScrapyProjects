# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagoujobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    city = scrapy.Field()
    companyName = scrapy.Field()
    companyId = scrapy.Field()
    positionName = scrapy.Field()
    positionId = scrapy.Field()
    salary = scrapy.Field()
    companyFullName = scrapy.Field()

    pass
