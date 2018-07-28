import requests
import execjs
import re
from urllib.parse import unquote, quote

def get_docx(htmlStr, htmlName, DocID):
    url = 'http://wenshu.court.gov.cn/Content/GetHtml2Word'
    headers = (
        {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*'
        }
    )
    data = {
        'htmlStr': htmlStr,
        'htmlName': htmlName,
        'DocID': DocID
    }
    # res = requests.get('http://wenshu.court.gov.cn/content/content', params={'DocID': DocID})

    with requests.post(url, data=data, headers=headers, stream=True) as r:
        with open(unquote(unquote(htmlName)) + '.docx', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx'
headers = (
    {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.139 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
)
doc_id = '532bd8ed-4ba8-48b7-ad70-0063f64ede05'
res = requests.get(url, params={'DocID': doc_id}, headers=headers)
text = res.text
r = re.findall(r'var jsonHtmlData.*', text)

raw = r[0]
# raw = raw.lstrip('var jsonHtmlData = \"')
# HtmlData = raw.rstrip('\";')
# raw = raw.replace('\\', '')
# data = json.loads(raw)
# text = res.text.replace('$', '')
# text = text.replace('\\', '')
default = execjs.get('jscript')
jsonHtmlData = raw + r'var jsonData = eval("(" + jsonHtmlData + ")");'
ect = default.compile(jsonHtmlData)
jsonData = ect.eval('jsonData')
title = jsonData['Title']
pub_date = jsonData['PubDate']
html = jsonData['Html']
Content = '''
                                <div id="contentTitle" style="text-align: center; line-height: 25pt; margin: 0.5pt 0cm;
                                    font-family: 黑体; font-size: 18pt;">''' + title + '''</div>
                                <div style="border-bottom: 1px dashed #BBBBBB; margin-bottom: 30px; height: 70px;">
                                    <div style="height: 20px; padding-top: 43px;">
                                        <table style="height: 20px; width: 100%;">
                                            <tbody><tr>
                                                <td style="font-size: 15px; font-family: '微软雅黑';text-align:left;" id="tdFBRQ">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发布日期：''' + pub_date + ''''</td>
                                                <td>
                                                </td>
                                                <td id="con_llcs" style="font-size: 15px; font-family: '微软雅黑';">浏览：0次</td>
                                                <td>
                                                    <ul>
                                                        <li style="display: inline;">
                                                            <img id="img_download" style="padding-top: 3px; cursor: pointer;" src="/Assets/img/content/download_small.png" alt="点击下载文书" onclick="lawyeeToolbar.Save.Html2Word();" data-bd-imgshare-binded="1">&nbsp; </li>
                                                        <li style="display: inline;">
                                                            <img id="img_print" style="padding-top: 3px; cursor: pointer;" src="/Assets/img/content/print_small.png" onclick="lawyeeToolbar.Print.PrintHtml()" alt="点击打印文书" data-bd-imgshare-binded="1">
                                                        </li>
                                                    </ul>
                                                </td>
                                            </tr>
                                        </tbody></table>
                                    </div>
                                </div>
                                    <div id="DivContent" style="TEXT-ALIGN: justify; text-justify: inter-ideograph; background: url('/Assets/img/content/bg_watermark.png') transparent;background-position-x: center;background-repeat-x: no-repeat;">''' + html + '''</div>'''
print(Content)
get_docx(quote(Content), title, doc_id)