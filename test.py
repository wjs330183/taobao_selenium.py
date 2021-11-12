import urllib.request

import requests
import json
import re

def print_hi(name):
    res = urllib.request.urlopen("https://www.qcc.com/cnews/bc80e695ea8504c3d2bed9cc5250ef03.html")
    r = requests.get("https://www.qcc.com/cnews/bc80e695ea8504c3d2bed9cc5250ef03.html")
    text = r.text
    status_code = r.status_code
    # json = r.json()
    cookies = r.cookies
    headers = r.headers
    rheaders = r.request.headers
    # print(r.text)
    print(rheaders)
    print(headers)
    print(cookies)
    print(r.status_code)
    # print(r.json())
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')
