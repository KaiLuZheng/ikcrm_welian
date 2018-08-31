#!/usr/bin/env python3/
# -*- coding: utf-8 -*-

from guiBase import signInBase
from guiBase import handleFiles


import logging

# it should be set on a config file, I do not want to set now
logging.basicConfig(level = logging.DEBUG,
                    format = '%(message)s'
)


# need delete
import urllib
import urllib.request
import http.cookiejar
import json,time
# need delete

from ikcrmRequestCore import ikcrmRequestCore

try:
    from dealExcelCore import dealExcelCore
except Exception as e:
    logging.error('import dealExcelCore error: %s'%e)

import threading

import re



import tkinter
# read txt, xlsx

TXT = 0
EXCEL = 1

ikcrm_base = ikcrmRequestCore()


# need to change a good idea
def charline(char, num):
    line = ''
    for i in range(0,num):
        line = line + char
    return line


def dict2list(dictionary):
    listt = []
    for item in dictionary:
        listt.append(dictionary[item])
    return listt
    

class ikcrmSearchInfo(handleFiles):
    def __init__(self):
        super().__init__(title='customer search', bnt1_text='load file', bnt2_text='check')
        
        self.topr.geometry("500x300+540+240")

        self.bnt3 = self.addBnt('check one number', self.bnt3event)
        self.bnt3.place(x = 150, y = 114)
        
        self.bnt3_entry = self.addEntry()
        self.bnt3_entry.place(x = 30, y = 114, width = 100)
   
        self.search = self.addText(width = 50, height = 7, state = 'normal')
        self.search.insert('end', 'You can check a number above.')
        self.search.config(state = 'disabled')
        self.search.place(x = 30, y = 164)

        self.bnt2.config(state = 'disabled')

        self.filetype = TXT
   
        self.ikcrm = ikcrm_base
        self.labels = ['phone_number', 'created_time', 'company', 'customer.name', 'project', 'user.name']


    def bnt1event(self):
        #filename = self.filepath([('txt','.txt'), ('excel','.xlsx')])
        filename = self.filepath([('txt','.txt')])
        #logging.debug('filepath: [%s]'%filename)
        
        self.bnt1_entry.config(state = 'normal')
        self.setEntry(self.bnt1_entry, filename)
        self.bnt1_entry.config(state = 'readonly')

        if re.search(r'\.txt$', filename) is not None: 
            self.filetype = TXT
            self.bnt2.config(state = 'normal')
        elif re.search(r'\.xlsx$', filename) is not None:
            self.filetype = EXCEL
            self.bnt2.config(state = 'normal')
        else: 
            self.filetype = -1
            self.bnt2.config(state = 'disabled')

        logging.debug('file type: %d'%self.filetype)

    def bnt2event(self):
        t = threading.Thread(target = self.bnt2event_thread)
        t.setDaemon(True)
        t.start()
        self.bnt2.config(state = 'disabled')
        self.bnt1.config(state = 'disabled')
        
        

    def bnt2event_thread(self):
        logging.debug('bnt start')
        filename = self.bnt1_entry.get()
        
        # check cookie
        cookiefile = 'mozilla_cookie.txt' 
        cookie = self.ikcrm.loadMozillaCookie(cookiefile)
        opener = self.ikcrm.buildOpener(cookie) 

        # read numbers not now
        if self.filetype == TXT:
            numbers = self.readTxt(filename)
        elif self.filetype == EXCEL:
            numbers = self.readExcel(filename)
           
        info_lists = []
        linesnumber = len(numbers)
        print('whole numbers: %d'%linesnumber)
        for num, number in enumerate(numbers):
            t1 = threading.Thread(target = self.checkCustomers, args = (number, info_lists))
            #t1.setDaemon(True)
            t1.start()

            percent = charline('#', int(35*num*1.0/linesnumber))
            t2 = threading.Thread(target = self.drawPercent, args = (percent,))
            #t3.setDaemon(True)
            t2.start()

            time.sleep(1) 
            #print('throw thread :at %d\r'%num)

       
        print('waiting finish.%d:%d'%(len(info_lists),len(numbers)))
        while True:
            if len(info_lists) == len(numbers):
                break
            else:
                print('waiting finish.%d:%d'%(len(info_lists),len(numbers)))
                time.sleep(1)
                continue

        t3 = threading.Thread(target = self.drawPercent, args = ('finished!',))
        t3.start()
        t3.join()
            
        self.bnt1.config(state = 'normal')
        
        # write in a txt at first
        # write in a excel


        try:
            self.writeExcel('outfile.xlsx', infos = info_lists)
        except Exception as e:
            print('write files: %s'%e)
            self.writeTxt('outfile.txt', infos = info_lists)
        


    def checkCustomers(self, number, info_lists):
        #logging.debug('start check:%s'%number)
        info = self.ikcrm.checkCustomers(number)
        if info is None:
            # deal with after
            labels = self.labels
            dict_empty = {}
            for i in labels:
                dict_empty[i] = ''
            dict_empty['phone_number'] = number
            info_lists.append(dict_empty)

            #for num, customer in enumerate(dict_empty):
            #    logging.debug('%s:%s'%(labels[num], dict_empty[customer]))
        else:
            info_lists.append(info)

        #print('info_lists:%d'%(len(info_lists)))
        #print(info_lists[-1])

    def drawPercent(self, percent):
        self.bnt2_entry.config(state = 'normal')
        self.setEntry(self.bnt2_entry, percent)
        self.bnt2_entry.config(state = 'readonly')
        

    def readTxt(self, filename):
        #logging.debug('need to read %s'%(filename,))
        with open(filename, 'r') as f:
            numbers = f.readlines()
        return numbers

    def writeTxt(self, filename, infos):
        # save number and user
        '''
        with open(filename, 'w') as f:
            for num, item in enumerate(infos):
                customer = str(num) + '\t' + item['phone_number'] + '\t' + item['user.name'] + '\n'
                f.write(customer)
        '''
        # save all infos
        with open(filename, 'w') as f:
            for num, item in enumerate(infos):
                f.write(str(num) + '\t')
                for i in item:
                    f.write(item[i]+'\t')
                f.write('\n')
        
        logging.debug('save as txt')

    def readExcel(self, filename):
        logging.debug('need to read %s'%(filename,))
        return 

    def writeExcel(self, filename, infos):

# last one
        self.writeTxt(filename, infos)
        sys.exit()

        sd = dealExcelCore()
        sd.setlabels(self.labels)

        for num, i in enumerate(infos):
            sd.setDate(num+2,dict2list(i))
            #print(num+2,':',dict2list(i))

        sd.saveExcel()
        logging.debug('save as excel')


    def bnt3event(self):
        number = (self.bnt3_entry.get())
        self.search.config(state = 'normal')
        self.clearText(self.search)
        self.search.insert('end', number)
        self.search.config(state = 'disabled')



class ikcrmSignIn(signInBase):
    def __init__(self, title, account):
        super().__init__(title, account)
        self.user_token = ''
        self.cookie = ''

        self.ikcrm = ikcrm_base
        
    def sign(self):
        login = self.login.get()
        password = self.pw.get()

        payload = {'login':login,'password':password,'device':'web'}
        req = self.ikcrm.buildPostRequest(payload)

        try:
            # save cookies
            r = self.ikcrm.simpleUrlopen(req)
            sjson = r.read().decode('UTF8')
            self.user_token = self.ikcrm.userToken(sjson)
            logging.debug('user_token:%s'%self.user_token)

            self.buildCookies(self.user_token)

            self.topr.destroy()
        except Exception as e:
            logging.error('sign error: %s'%e)
            self.topr.title('sign faild!')

    def buildCookies(self, user_token):
        cookie_filename = 'mozilla_cookie.txt'
        cookie = self.ikcrm.buildMozillaCookie(cookie_filename)
        opener = self.ikcrm.buildOpener(cookie)

        param = {'user_token':user_token}

        req = self.ikcrm.buildHomeRequest(param)
        try:
            res = opener.open(req)
            page = res.read().decode()
        except urllib.error.URLError as e:
            logging.error(e.code, ':', e.reason)

        cookie.save(ignore_discard = True, ignore_expires=True)

        

if __name__ == '__main__':
    t = {'1':1, '2':2, '3':3}
    print(dict2list(t))

