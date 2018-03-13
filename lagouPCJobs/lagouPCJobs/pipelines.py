# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class LagoupcjobsPipeline(object):
    def process_item(self, item, spider):
        if item == None:
            return item
        # 将experience内容合并去掉'\n'
        combineKey = ''
        for key in item['experience']:
            combineKey += key
        item['experience'] = combineKey.replace('\n', '')
        item['experience'] = item['experience'].strip()
        # 将tag内容合并
        combineKey = ''
        for key in item['tag']:
            combineKey += key
            combineKey += ', '
        item['tag'] = combineKey[:-2]
        # 将type内容去掉'\n'
        item['type'] = item['type'].replace('\n', '')
        item['type'] = item['type'].strip()
        with open('jobs.csv', 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(item[key] for key in item)
        return item
