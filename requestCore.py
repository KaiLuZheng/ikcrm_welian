#!/usr/bin/env python3
# -*- coding: utf-8 -*-


try:
    import urllib
    import urllib.request as urequest
    import http.cookiejar
except Exception as e:
    logging.error('you use python2.x: %s'%e)
    import urllib
    import urllib2 as urequest    

import json,time


class requestCore():
    headers = {}
    def __init__(self):
        self.opener = urequest.build_opener()
        pass
    

    def simpleUrlopen(self, req):
        return urequest.urlopen(req)

    def buildPostRequestCore(self, url = None, payload = None, headers = None):
        data = urllib.parse.urlencode(payload).encode(encoding = 'UTF8')
        if headers is None:
            req = urequest.Request(url, data)
        else:
            req = urequest.Request(url, data, headers = headers)
        return req
    

    def buildMozillaCookie(self, cookie_filename = 'mozilla_cookie.txt'):
        return http.cookiejar.MozillaCookieJar(cookie_filename) 

    def loadMozillaCookie(self, cookie_filename = 'mozilla_cookie.txt'):
        cookie = http.cookiejar.MozillaCookieJar()
        cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
        return cookie

    def buildOpener(self, cookie = None):
        if cookie is None:
            return False

        # check type , but i do not want to do now
        handler = urequest.HTTPCookieProcessor(cookie)
        self.opener = urequest.build_opener(handler)
        return self.opener
        
        

