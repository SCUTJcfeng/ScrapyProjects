# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class LagoujobsPipeline(object):
    def process_item(self, item, spider):
        headers = ['city', 'companyFullName', 'companyId', 'companyName', 'positionId', 'positionName', 'salary']
        with open('position.csv', 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(item[key] for key in item)
        return item
