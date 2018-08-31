#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib
import urllib.request
import http.cookiejar

import json,time


class requestCore():
    headers = {}
    def __init__(self):
        self.opener = urllib.request.build_opener()
        pass
    

    def simpleUrlopen(self, req):
        return urllib.request.urlopen(req)

    def buildPostRequestCore(self, url = None, payload = None, headers = None):
        data = urllib.parse.urlencode(payload).encode(encoding = 'UTF8')
        if headers is None:
            req = urllib.request.Request(url, data)
        else:
            req = urllib.request.Request(url, data, headers = headers)
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
        handler = urllib.request.HTTPCookieProcessor(cookie)
        self.opener = urllib.request.build_opener(handler)
        return self.opener
        
        

