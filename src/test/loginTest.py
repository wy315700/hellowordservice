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
        self.url = 'http://halloword.sinaapp.com/user/login.json'

    def test_failed_json(self):

        values ={'parms' : ' \
        {\
            "request" : "/user/login.json",\
            "loginInfo" : {\
                "userName" : "aaa",\
                "password" : "aaaaaa"\
            }\
        '}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        try:
            req = urllib2.Request(self.url, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            self.assertIn('failed',response.read())
        except urllib2.HTTPError, e:
            print e.code
            self.assertEqual(1,0)
        except urllib2.URLError, e:
            print e.reason

    def test_failed_params(self):

        values ={'params' : ' \
        {\
            "requestss" : "/user/login.json",\
            "loginInfo" : {\
                "userName" : "aaa",\
                "password" : "aaaaaa"\
            }\
        }\
        '}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        try:
            req = urllib2.Request(self.url, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            self.assertIn('failed',response.read())
        except urllib2.HTTPError, e:
            print e.code
            self.assertEqual(1,0)
        except urllib2.URLError, e:
            print e.reason

    def test_success_login(self):

        values ={'params' : ' \
        {\
            "request" : "/user/login.json",\
            "loginInfo" : {\
                "userName" : "123",\
                "password" : "aaaaaa"\
            }\
        }\
        '}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        try:
            req = urllib2.Request(self.url, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            self.assertIn('success',response.read())
        except urllib2.HTTPError, e:
            print e.code
            self.assertEqual(1,0)
        except urllib2.URLError, e:
            print e.reason


    def test_failed_login(self):

        values ={'params' : '''
        {
            "request" : "/user/login.json",
            "loginInfo" : {
                "userName" : "a",
                "password" : "aaaaaa"
            }
        }
        '''}
        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        try:
            req = urllib2.Request(self.url, data)
            response = urllib2.urlopen(req)
            httpcode = response.getcode()
            self.assertEqual(httpcode,200)
            self.assertIn('failed',response.read())
        except urllib2.HTTPError, e:
            print e.code
            self.assertEqual(1,0)
        except urllib2.URLError, e:
            print e.reason


if __name__ == '__main__':
    unittest.main()
