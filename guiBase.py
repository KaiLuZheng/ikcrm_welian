#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging


try:
    import tkinter
    from tkinter import *
    import tkinter.filedialog as filedialog
except Exception as e:
    logging.error('your use python2.x: %s'%e)
    import Tkinter as tkinter
    from Tkinter import *
    import tkFileDialog as filedialog


class handleFiles():
    def __init__(self, title, bnt1_text, bnt2_text):
        top = tkinter.Tk()
        top.geometry("500x200+540+240") 
        top.title(title)
        top.resizable(0,0)

        bnt1 = Button(top,
                      text=bnt1_text,
                      width = 10,
                      command = self.bnt1event)
        bnt2 = Button(top,
                      text=bnt2_text,
                      width = 10,
                      command = self.bnt2event)

        wth = 33
        bnt1_entry = Entry(top,
                           width = wth,
                           state = 'readonly')

        bnt2_entry = Entry(top,
                           width = wth,
                           state = 'readonly')
                          # state = 'normal') # 35 #
       
        bnt1.place(x = 30, y = 24) 
        bnt2.place(x = 30, y = 64)
        bnt1_entry.place(x = 150, y = 24)
        bnt2_entry.place(x = 150, y = 64)

        self.topr = top
        self.bnt1 = bnt1
        self.bnt2 = bnt2
        self.bnt1_entry = bnt1_entry
        self.bnt2_entry = bnt2_entry
        
    def bnt1event(self):
        pass

    def bnt2event(self):
        pass
       
    def bnt3event(self):
        pass

    def addEntry(self, state='normal'):
        entry = Entry(self.topr,
                      state = state) 
        return entry

    def addText(self, width = 30, height = 2, state='normal'):
        text = Text(self.topr,
                    width = width,
                    height = height,
                    state = state)

        return text


    def addBnt(self, text, func):
        bnt = Button(self.topr,
                     text = text,
                     command = func)
        return bnt

    def clearText(self, text_handle):
        text_handle.delete(0.0, tkinter.END)

    def filepath(self, filetype):
        #return tkinter.filedialog.askopenfilename(filetypes=filetype)
        return filedialog.askopenfilename(filetypes=filetype)

    def clearEntry(self, entry_handle):
        entry_handle.delete(0, tkinter.END)

    def add2Entry(self, entry_handle, text):
        entry.insert(tkinter.END, text)
 
    def setEntry(self, entry, text):
        self.clearEntry(entry)
        entry.insert(tkinter.END, text)

    def run(self):
        self.topr.mainloop()


class signInBase():
    def __init__(self, title, account):
        top = tkinter.Tk()
        top.geometry("300x130+540+240")
        top.title(title)
        top.resizable(0,0)

        login_label = Label(top,
                            text=account)

        pw_label = Label(top,
                         text='密码')

        login = Entry(top,
                      width = 10)

        pw = Entry(top,
                   width = 10,
                   show = '*')

        sign_in = Button(top,
                         text='sign',
                         width=10,
                         command=self.sign)


        # 要用相对位置，现在先不管
        login_label.place(x = 30, y = 24)
        login.place(x = 150, y = 20)

        pw_label.place(x = 30, y = 54)
        pw.place(x = 150, y = 50)

        sign_in.place(x = 98, y = 88)

        self.topr = top
        self.login = login
        self.pw = pw

    def sign(self):
        pass

    def run(self):
        self.topr.mainloop()


