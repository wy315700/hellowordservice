# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  longpollTest.m
#  helloword
#
#  Created by 汪 洋 on 14-2-26.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import unittest
import urllib,urllib2
import multiprocessing
import time

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.get_message_url = 'http://127.0.0.1:8000/helloword/get_message.json'
        self.new_message_url = 'http://127.0.0.1:8000/helloword/new_message.json'

    def test_case(self):
        get_message = multiprocessing.Process(name='get_message',
                                      target=self.get_message)

        new_message = multiprocessing.Process(name='new_message',
                                      target=self.new_message)

        get_message.start()
        time.sleep(2)
        new_message.start()

    def get_message(self):

        values ={'params' : '\
        {\
        "request" : "/helloword/get_message.json",\
        "sessionID" : "ac52f2a4-a9e4-4ebc-baf7-e91ec37d7d72"\
        }\
        '}
        data = urllib.urlencode(values)
        try:
            req = urllib2.Request(self.get_message_url, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            self.assertIn('success',response.read())
        except urllib2.HTTPError, e:
            print e.code
            self.assertEqual(1,0)
        except urllib2.URLError, e:
            print e.reason

    def new_message(self):

        values ={'params' : ' \
        {\
        "request" : "/helloword/new_message.json",\
        "toSessionID" : "all",\
        "messageType" : "1",\
        "title" : "2",\
        "content" : "3"\
        }\
        '}
        data = urllib.urlencode(values)
        try:
            req = urllib2.Request(self.new_message_url, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            self.assertIn('success',response.read())
        except urllib2.HTTPError, e:
            print e.code
            self.assertEqual(1,0)
        except urllib2.URLError, e:
            print e.reason



if __name__ == '__main__':
    unittest.main()
