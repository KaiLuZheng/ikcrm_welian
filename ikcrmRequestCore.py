#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
logging.basicConfig(level = logging.ERROR,
                    format = '%(message)s'
)

try:
    import urllib
    import urllib.request
    import http.cookiejar
except Exception as e:
    logging.error('you use python2.x: %s'%e)


import json,time

from requestCore import requestCore


class ikcrmRequestCore(requestCore):
    login_url = 'https://dingtalk.e.ikcrm.com/api/v2/auth/login' # post login 
    home_url = 'https://dingtalk.e.ikcrm.com/dingtalk/sessions/new?' # get sign in token
    search_head_url = 'https://dingtalk.e.ikcrm.com/duplicate/search?' # check customer

    user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

    def __init__(self):
        self.user_token = ''
        self.cookies = ''
        pass


    def checkCustomers(self, number):
#        logging.debug('numbers:%s'%number)
        param = {'key':'customer'}

        param['query'] = number
        search_url = self.search_head_url + urllib.parse.urlencode(param)
        # logging.debug('search url: %s'%search_url)

        req = urllib.request.Request(search_url, headers = self.headers)
        #  opener open check
        res = self.opener.open(req)
        sjson = res.read().decode()

        try:
            cus_dict = json.loads(sjson)[0]
        except Exception as e:
            logging.error('error.checkCustomers: %s:%s'%(e,number))
            return None
#        print(cus_dict)

        info = {}
        info['phone_number'] = cus_dict['address.phone']
        info['created_time'] = cus_dict['created_at']
        info['company'] = cus_dict['name']
        info['customer.name'] = cus_dict['text_asset_88c8ce2e']
        info['project'] = cus_dict['text_asset_b7bbd60d']
        info['user.name'] = cus_dict['user.name']

        labels = ['phone_number', 'created_time', 'company', 'customer.name', 'project','user.name']

#        for num, customer in enumerate(info):
#            logging.debug('%s:%s'%(labels[num], info[customer]))
        
        return info

        '''
        address.phone: "13142256056"        # phone number
        company_name : "" 
        created_at : "2017-12-19 09:25"     # created_time
        id : 28648819                       # page id: http://dingtalk.e.ikcrm.com/customers/ + id
        is_allow_grab : null
        is_common_customer : false
        is_invisible : false
        name : "13142256056"                # company 
        own : true
        text_asset_88c8ce2e : "刘欣"        # name of customer
        text_asset_b7bbd60d : "综合电商？"  # project of customer
        user.name : "罗仕海"                # adviser
        '''



    def buildHomeRequest(self, param = None):
        if param is None:
            return False
        url = self.home_url+urllib.parse.urlencode(param)
        return urllib.request.Request(url, headers = self.headers) 
        

    def userToken(self, sjson):
        try:
            self.user_token = json.loads(sjson)['data']['user_token']
        except Exception as e:
            logging.error('error: ikcrmReqeustCore.userToken promblem %s'%e)
            raise Exception('gain token failed error')
        
        return self.user_token

    def buildPostRequest(self, payload):
        return self.buildPostRequestCore(self.login_url, payload)












