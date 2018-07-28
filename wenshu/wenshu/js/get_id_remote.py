import requests
import json
import random
import execjs
import pymysql
import redis


class IdSpider(object):
    def __init__(self):
        super().__init__()
        self.db = pymysql.connect(host='rm-wz9wj90j9qzcfasz6.mysql.rds.aliyuncs.com', user='root', port=3306, password='qazwsx12!@',
                                  database='wenshu', charset='utf8')
        self.create_table()
        self.url = 'http://wenshu.court.gov.cn/List/ListContent'
        self.param = ''
        self.index = 1
        self.page = 20
        self.order = '法院层级'
        self.direction = 'asc'
        self.USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 Safari/537.36'
        ]

    def get_content(self, Param='', Index=1, Page=5, Order='法院层级', Direction='asc', vl5x=None, number=None, guid=None,
                    vjkl5=None):
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        headers = (
            {
                'user-agent': random.choice(self.USER_AGENTS),
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        )
        cookies = {
            'vjkl5': vjkl5
        }
        data = {
            'Param': Param,
            'Index': Index,
            'Page': Page,
            'Order': Order,
            'Direction': Direction,
            'vl5x': vl5x,
            'number': number,
            'guid': guid
        }
        res = requests.post(url, data=data, headers=headers, cookies=cookies)
        return res.text

    def get_code(self, guid):
        url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
        s = requests.Session()
        s.headers.update(
            {
                'user-agent': random.choice(self.USER_AGENTS),
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
                'user-agent': random.choice(self.USER_AGENTS),
            }
        )
        res = requests.get(url, headers=headers)
        return res.cookies['vjkl5']

    def create_table(self):
        sql = '''CREATE TABLE
        IF
            NOT EXISTS `wenshu_id` (
            `paperId` VARCHAR ( 36 ) NOT NULL,
            `name` VARCHAR ( 255 ) NOT NULL,
            `content` text NOT NULL,
            `type` VARCHAR ( 8 ) NOT NULL,
            `date` VARCHAR ( 15 ) NOT NULL,
            `procedure` VARCHAR ( 20 ) NOT NULL,
            `anhao` VARCHAR ( 50 ) NOT NULL,
            `courtName` VARCHAR ( 50 ) NOT NULL,
            PRIMARY KEY ( `paperId` ) 
            ) ENGINE = INNODB DEFAULT CHARSET = utf8'''
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()

    def save_to_table(self, paperId, name, content, type, date, procedure, anhao, courtName):
        sql = '''INSERT INTO wenshu_id (paperId, `name`, content, `type`, `date`, `procedure`, anhao, courtName) VALUES 
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % \
              (paperId, name, content, type, date, procedure, anhao, courtName)
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            self.db.commit()

if __name__ == '__main__':
    while True:
        r = redis.Redis(host='127.0.0.1', port=6388, password='qazwsx12!@')
        # r.lpush('wenshu:id', 74)
        idx = r.lpop('wenshu:id')
        index = int(idx)
        print(index)
        with open('./process.js', 'r') as f:
            default = execjs.get('phantomjs')
            data = f.read()
            ect = default.compile(data)
            guid = ect.call('getGuid')
            so = IdSpider()
            number = so.get_code(guid)
            vjkl5 = so.get_vjkl5()
            vl5x = ect.call('getKey', vjkl5)
            text = so.get_content(Index=index, Page=20, Order='法院层级', Direction='asc', vl5x=vl5x, number=number, guid=guid,
                               vjkl5=vjkl5)
            text_pro = text.replace('\\', '')
            text_pro = text_pro.lstrip('\"')
            text_pro = text_pro.rstrip('\"')
            data = json.loads(text_pro)
            if data != '':
                del data[0]
                for case in data:
                    item = {}
                    try:
                        item['content'] = case['裁判要旨段原文']
                    except:
                        item['content'] = ''
                    item['type'] = case['案件类型']
                    item['date'] = case['裁判日期']
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
                    try:
                        so.save_to_table(item['paperId'], item['name'], item['content'], item['type'],
                               item['date'], item['procedure'], item['anhao'], item['courtName'])
                    except Exception as e:
                        print(e)