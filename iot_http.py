import requests
import time
import hashlib
import urllib.request
import json


def getToken(appKey, appSecret):
    millis = str(int(round(time.time() * 1000)))
    appToken = hashlib.md5((appKey + appSecret + millis).encode()).hexdigest()
    r = requests.get(
        "https://tsgz.zjamr.zj.gov.cn:8181/getToken?" + "appKey=" + appKey + "&appToken=" + appToken + "&timestamp=" + millis)
    text = r.text
    data = json.loads(text)
    token = data.get("data").get("token")
    status_code = r.status_code
    headers = r.headers
    print(text)
    print(status_code)
    print(headers)
    return token


def uploadIotData(token, param):
    url = "https://tsgz.zjamr.zj.gov.cn:8181//uploadIotData/n"
    millis = int(round(time.time() * 1000))
    headers = {
        'Host': 'tsgz.zjamr.zj.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Token': token,
        'Timestamp': millis
    }
    try:
        params = urllib.parse.urlencode(param).encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        r = urllib.request.urlopen(req)
        html = r.read()
        status = r.status
        version = r.version
        msg = r.msg
        print(status)
        print(version)
        print(msg)
        return html
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))


if __name__ == '__main__':
    appKey = '323bda78d1a1492f8d92e72036c84ba3'
    appSecret = '5491d652348446c7ad96341a9e76484a'
    tokens = getToken(appKey, appSecret)

    str = '{"equCode": "3110Z0110201900055","idCode": "330102199911232114,330102199911232115","data": [{"time": "2021-07-25 12:05:15","y01": 220,"y02": 220.5,"y03": 219,"y04": 10,"y05": 10.5,"y06": 11,"y07": 30},{"time": "2021-07-25 12:06:15","y01": 222,"y02": 221,"y03": 211.5,"y04": 11,"y05": 12,"y06": 11.5,"y07": 40}]}'
    dataDsr = json.loads(str)
    uploadIotData(tokens, dataDsr)
