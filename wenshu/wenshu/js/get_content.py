import requests
import execjs
import json

def get_code(guid):
    url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
    s = requests.Session()
    s.headers.update(
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    )
    data = {
        'guid': guid
    }
    res =  s.post(url, data=data)
    return res.text

def get_content(Param='', Index=1, Page=5, Order='法院层级', Direction='asc', vl5x=None, number=None, guid=None, vjkl5=None):
    url = 'http://wenshu.court.gov.cn/List/ListContent'
    headers = (
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
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

def get_vjkl5():
    url = 'http://wenshu.court.gov.cn/list/list/?sorttype=1'
    headers = (
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
        }
    )
    res = requests.get(url, headers=headers)
    return res.cookies['vjkl5']

default = execjs.get('phantomjs')
with open('./js/process.js', 'r') as f:
    data = f.read()
    ect = default.compile(data)
    guid = ect.call('getGuid')
    number = get_code(guid)
    vjkl5 = get_vjkl5()
    vl5x = ect.call('getKey', vjkl5)
    text = get_content(Index=2, Page=20, Order='法院层级', Direction='asc', vl5x=vl5x, number=number, guid=guid, vjkl5=vjkl5)
    text_pro = text.replace('\\', '')
    text_pro = text_pro.lstrip('\"')
    text_pro = text_pro.rstrip('\"')
    data = json.loads(text_pro)
    if data != '':
        del data[0]
        for case in data:
            print(case)

    print(text)