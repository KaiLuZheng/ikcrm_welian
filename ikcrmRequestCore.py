#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging

try:
    import urllib
    import urllib.request
    import http.cookiejar
except Exception as e:
    logging.error('you use python2.x: %s'%e)


import json,time

from requestCore import requestCore

import re
import sys

from labels import project_labels as labels


class ikcrmRequestCore(requestCore):
    login_url = 'https://dingtalk.e.ikcrm.com/api/v2/auth/login' # post login 
    home_url = 'https://dingtalk.e.ikcrm.com/dingtalk/sessions/new?' # get sign in token
    search_head_url = 'https://dingtalk.e.ikcrm.com/duplicate/search?' # check customer
    search_all_url = 'http://dingtalk.e.ikcrm.com/customers/' # check customer all infos + id
    search_api_url = "https://dingtalk.e.ikcrm.com/api/v2/customers?" # + number
    base_info = 'https://dingtalk.e.ikcrm.com/customers/%s?only_base_info=true'

    '''
        params = {"user_token":self.user_token,"device":"dingtalk","version_code":"3.3.0"}
        params["query"] = checkinfo
        time.sleep(1)

# need change 
        data = urllib.parse.urlencode(params).encode(encoding='UTF8')
        req = urllib.request.Request(url+'?'+data.decode('utf8'))

    '''


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

        #labels = ['phone_number', 'created_time', 'company', 'customer.name', 'project','user.name','status','updated_at','lastest.content']

        for num, customer in enumerate(info):
            logging.debug('%s:%s'%(labels[num], info[customer]))



        try:
            others = self.dealWithAllInfo(str(cus_dict['id']), str(cus_dict['address.phone']))
        except Exception as e:
            logging.error('error file: %s'%__file__)
            logging.error('dealWithAllInfo.error: %s:%s'%(e,cus_dict['address.phone']))

        
        info.update(others)
        
        return info


    def dealWithAllUpdates(self, num_id): 

        '''
        发现在内存中的这个，更加合适获取跟进信息 
        '''
        url = self.base_info%num_id
        headers = self.headers
        headers['X-Requested-With'] = 'XMLHttpRequest'

        req = urllib.request.Request( url , headers = headers)
        res = self.opener.open(req)
        html = res.read().decode('utf8')

        with open('test.xml', 'w') as f:
            f.write(html)




    def dealWithAllInfo(self, num_id, number): # the old one what use search customer page 
        #req = urllib.request.Request(self.search_all_url + num_id, headers = self.headers)  # a page of customer
        host_url = 'http://dingtalk.e.ikcrm.com/customers?'

        headers = self.headers
        headers['Referer'] = 'http://dingtalk.e.ikcrm.com/customers'

        param = {}
        param = {'search_key':number} # number
        param['section_only'] = 'true'
        url = host_url + urllib.parse.urlencode(param)

        logging.debug('url: %s'%url)

        req = urllib.request.Request( url , headers = headers)
        res = self.opener.open(req)
        html = res.read().decode()
    
        infos = {}


# id=47158877
        a = re.search(r'<tr class(.*?)%s">(.*?)</tr>'%(num_id), html, re.S)
# status
        b = re.search(r'"status_mapped">(.*?)</td>', a.group(), re.S)
        c = re.search(r'"value">(.*?)</div>', b.group(), re.S)
        logging.debug('status:') 
        logging.debug(c.group(1).replace('\n', '').replace(' ', ''))
        infos['status'] = (c.group(1).replace('\n', '').replace(' ', ''))

# updated_at
        b = re.search(r'real_revisit_at">(.*?)</td>', a.group(), re.S)
        c = re.search(r'datetime=(.*?)>(.*?)</time>', b.group(), re.S)
        logging.debug('updated_at:')
        logging.debug(c.group(2).replace(' ', '-'))
        infos['updated_at'] = (c.group(2).replace(' ', '-'))

# lastest_revisit_log.content
        logging.info('crap revisit...')

        b = re.search(r'lastest_revisit_log.content">(.*?)</td>', a.group(), re.S)

        try: 
            c = re.search(r'data-content(.*?)>(.*?)</div>', b.group(), re.S)
            logging.debug(c.group(2))
        except Exception as e:
            logging.error('page changed, cannot crap revisit_log: %s'%e)
            logging.error('error: %s'%__file__)
            infos['lastest.content'] = 'crap failed.'
            logging.debug('crap end')
        else:
            try:
                infos['lastest.content'] = (c.group(2).replace('\n','').replace('\r',''))
            except Exception as e:
                logging.error('lastest content.error: %s:%s'%(e,number))
                infos['lastest.content'] = ''
            
        logging.info('crap revisit end ')

        logging.debug(infos)


        return infos




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






if __name__ == '__main__':

    '''

    with open('18618459162.html') as f:
        html = f.read()

# id=47158877
    a = re.search(r'<tr class(.*?)%s">(.*?)</tr>'%(str(47158877)), html, re.S)
# status
    b = re.search(r'"status_mapped">(.*?)</td>', a.group(), re.S)
    c = re.search(r'"value">(.*?)</div>', b.group(), re.S)
    print(c.group(1).replace('\n', '').replace(' ', ''))

# updated_at
    b = re.search(r'real_revisit_at">(.*?)</td>', a.group(), re.S)
    c = re.search(r'datetime=(.*?)>(.*?)</time>', b.group(), re.S)
    print(c.group(2).replace(' ', '-'))

# lastest_revisit_log.content
    b = re.search(r'lastest_revisit_log.content">(.*?)</td>', a.group(), re.S)
    c = re.search(r'data-content(.*?)>(.*?)</div>', b.group(), re.S)
    print(c.group(2))

    sys.exit()
    '''

    '''
    A = ikcrmRequestCore()
    cookiefile = 'mozilla_cookie.txt'
    cookie = A.loadMozillaCookie(cookiefile)

    A.buildOpener(cookie)
    #A.checkCustomers('15900628966')
    A.dealWithAllUpdates('41840717')
   
    ''' 

    with open('test.html') as f:
        html = f.read()

    a = re.search(r'updated_at(.*?)time>', html, re.S).group()
    b = re.search(r'datetime=(.*?)time', a, re.S).group()
    c = re.search(r'>(.*?)<', b, re.S).group(1)
    print(c)



