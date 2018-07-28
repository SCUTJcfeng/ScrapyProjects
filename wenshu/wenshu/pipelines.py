# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from wenshu.settings import *

class WenshuPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PASSWORD,
                                  database=MYSQL_DB, charset='utf8')
        self.create_table()

    def create_table(self):
        sql = '''CREATE TABLE
        IF
            NOT EXISTS `wenshu_id` (
            `paperId` VARCHAR ( 36 ) NOT NULL,
            `name` VARCHAR ( 255 ) NOT NULL,
            `content` text NOT NULL,
            `type` INT ( 2 ) NOT NULL,
            `date` date NOT NULL,
            `procedure` VARCHAR ( 20 ) NOT NULL,
            `anhao` VARCHAR ( 50 ) NOT NULL,
            `courtName` VARCHAR ( 50 ) NOT NULL,
            PRIMARY KEY ( `paperId` ) 
            ) ENGINE = INNODB DEFAULT CHARSET = utf8'''
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()

    def drop_table(self):
        sql = '''DROP TABLE IF EXISTS `comments`'''
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()

    def save_to_table(self, paperId, name, content, type, date, procedure, anhao, courtName):
        sql = '''INSERT INTO wenshu_id (paperId, `name`, content, `type`, `date`, `procedure`, anhao, courtName) VALUES 
                ('%s', '%s', '%s', %d, '%s', '%s', '%s', '%s')''' % \
              (paperId, name, content, type, date, procedure, anhao, courtName)
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()

    def process_item(self, item, spider):
        if spider.name == 'id':
            self.save_to_table(item['paperId'], item['name'], item['content'], int(item['type']),
                               item['date'], item['procedure'], item['anhao'], item['courtName'],)
        return item
