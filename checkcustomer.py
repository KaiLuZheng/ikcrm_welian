#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

# it should be set on a config file, I do not want to set now
logging.basicConfig(level = logging.DEBUG,
                    format = '%(message)s'
)

import urllib
import urllib.request
import http.cookiejar

import json,time

import _thread


url = 'https://dingtalk.e.ikcrm.com/duplicate/search'
url = 'http://dingtalk.e.ikcrm.com/duplicate/search?key=customer&query=13366006234'


login_url = 'https://dingtalk.e.ikcrm.com/api/v2/auth/login'

payload={"login": "18767106508","password": "1991350zklZ", 'device':'web'}

data = urllib.parse.urlencode(payload).encode(encoding='UTF8')
req = urllib.request.Request(login_url, data)
r = urllib.request.urlopen(req)
sjson = r.read().decode('utf8')
user_token=json.loads(sjson)['data']['user_token']

home_url = 'https://dingtalk.e.ikcrm.com/dingtalk/sessions/new?' # user_token=7658bad3630ab262ffdaa03cc08e63d7

user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

param = {'user_token':user_token}
url = home_url+urllib.parse.urlencode(param)
req = urllib.request.Request(url, headers=headers)

try:
    res = opener.open(req)
    page = res.read().decode()
except urllib.error.URLError as e:
    logging.error(e.code, ':', e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中


url = 'http://dingtalk.e.ikcrm.com/duplicate/search?key=customer&query=13366006234'
req = urllib.request.Request(url, headers=headers)
res = opener.open(req)
page = res.read().decode()
print(page)


