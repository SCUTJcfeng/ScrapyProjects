import requests
import execjs
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
}
res = requests.get('http://wenshu.court.gov.cn/Assets/js/Lawyee.CPWSW.DictData.js', headers = headers)

default = execjs.get('jscript')
ect = default.compile(res.text)
data = ect.eval('ayData')
data_json = json.dumps(data, ensure_ascii=False, indent=4)
with open('dict.json', 'w+', encoding='utf8') as f:
    f.write(data_json)
# print(data)