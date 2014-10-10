# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  LoginHandler.m
#  helloword
#
#  Created by 汪 洋 on 14-1-24.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import unittest
import urllib,urllib2


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/helloword/request_pk_game.json'
        self.url2 = 'http://127.0.0.1:8000/helloword/upload_pk_result.json'
        self.url3 = 'http://halloword.sinaapp.com/helloword/request_rank.json'

    # def test_success_request(self):

    #     values ={'params' : ' \
    #     {\
    #     "request" : "/helloword/request_pk_game.json",\
    #     "sessionID"  : "a0badbdb-0fa6-4090-bdbc-3765cc6a9afc",\
    #     "gameType" : "1" \
    #     }\
    #     '}
    #     data = urllib.urlencode(values)
    #     req = urllib2.Request(self.url, data)
    #     try:
    #         req = urllib2.Request(self.url, data)
    #         response = urllib2.urlopen(req)
    #         httpcode = response.getcode()
    #         self.assertEqual(httpcode,200)
    #         print response.read()
    #         # self.assertIn('success',response.read())

    #     except urllib2.URLError, e:
    #         print e.reason

    # def test_success_upload(self):

    #     values ={'params' : ' \
    #     {\
    #     "request" : "/helloword/upload_pk_result.json",\
    #     "sessionID" : "a0badbdb-0fa6-4090-bdbc-3765cc6a9afc",\
    #     "gameID"  : "aa",\
    #     "userAnswer":[\
    #       {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #       {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #       {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "a",\
    #         "time"   : "5"\
    #         },\
    #         {\
    #         "ans" : "necessity",\
    #         "time"   : "5"\
    #         }\
    #     ]\
    #     }\
    #     '}
    #     data = urllib.urlencode(values)
    #     try:
    #         req = urllib2.Request(self.url2, data)
    #         response = urllib2.urlopen(req)
    #         httpcode = response.getcode()
    #         self.assertEqual(httpcode,200)
    #         print response.read()
    #         # self.assertIn('success',response.read())

    #     except urllib2.URLError, e:
    #         print e.reason

    def test_success_request_rank(self):

        values ={'params' : ' \
        {\
        "request" : "/helloword/request_rank.json",\
        "sessionID"  : "26c218b9-a2e2-48e8-b81c-8f08ec2b5c47"\
        }\
        '}
        data = urllib.urlencode(values)
        # req = urllib2.Request(self.url3, data)
        try:
            req = urllib2.Request(self.url3, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            print response.read()
            # self.assertIn('success',response.read())

        except urllib2.URLError, e:
            print e.reason


if __name__ == '__main__':
    unittest.main()
