# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  changeInfoTest.m
#  helloword
#
#  Created by 汪 洋 on 14-2-2.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import unittest
import urllib,urllib2

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/user/change_userinfo.json'

    # def test_failed_json(self):

    #     values ={'parms' : ' \
    #     {\
    #         "request" : "/user/change_userinfo.json",\
    #         "sessionID" : "sessionID",\
    #         "userInfo" : {\
    #             "userName" : "userName",\
    #             "userNickname" : "userNickname",\
    #             "oldPassword" : "oldPassword",\
    #             "newPassword" : "newPassword"\
    #         }\
    #     }\
    #     '}
    #     data = urllib.urlencode(values)
    #     req = urllib2.Request(self.url, data)
    #     try:
    #         req = urllib2.Request(self.url, data)
    #         response = urllib2.urlopen(req)
    #         httpcode = response.getcode()
    #         self.assertEqual(httpcode,200)
    #         self.assertIn('failed',response.read())
    #     except urllib2.HTTPError, e:
    #         print e.code
    #         self.assertEqual(1,0)
    #     except urllib2.URLError, e:
    #         print e.reason

    # def test_failed_params(self):

    #     values ={'params' : ' \
    #     {\
    #         "equest" : "/user/change_userinfo.json",\
    #         "sessionID" : "sessionID",\
    #         "userInfo" : {\
    #             "userName" : "userName",\
    #             "userNickname" : "userNickname",\
    #             "oldPassword" : "oldPassword",\
    #             "newPassword" : "newPassword"\
    #         }\
    #     }\
    #     '}
    #     data = urllib.urlencode(values)
    #     req = urllib2.Request(self.url, data)
    #     try:
    #         req = urllib2.Request(self.url, data)
    #         response = urllib2.urlopen(req)
    #         httpcode = response.getcode()
    #         self.assertEqual(httpcode,200)
    #         self.assertIn('failed',response.read())
    #     except urllib2.HTTPError, e:
    #         print e.code
    #         self.assertEqual(1,0)
    #     except urllib2.URLError, e:
    #         print e.reason

    def test_success_change_info(self):

        values ={'params' : ' \
        {\
            "request" : "/user/change_userinfo.json",\
            "sessionID" : "a0badbdb-0fa6-4090-bdbc-3765cc6a9afc",\
            "userInfo" : {\
                "userName" : "123",\
                "userNickname" : "333",\
                "oldPassword" : "aaaaaa",\
                "newPassword" : "aaaaaa",\
                "userAvatarType" : "id",\
                "userAvatar" : "3"\
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

    # def test_failed_change_info(self):

    #     values ={'params' : ' \
    #     {\
    #         "request" : "/user/change_userinfo.json",\
    #         "sessionID" : "sessionID",\
    #         "userInfo" : {\
    #             "userName" : "userName",\
    #             "userNickname" : "userNickname",\
    #             "oldPassword" : "oldPassword",\
    #             "newPassword" : "newPassword"\
    #         }\
    #     }\
    #     '}
    #     data = urllib.urlencode(values)
    #     req = urllib2.Request(self.url, data)
    #     try:
    #         req = urllib2.Request(self.url, data)
    #         response = urllib2.urlopen(req)
    #         httpcode = response.getcode()
    #         self.assertEqual(httpcode,200)
    #         self.assertIn('failed',response.read())
    #     except urllib2.HTTPError, e:
    #         print e.code
    #         self.assertEqual(1,0)
    #     except urllib2.URLError, e:
    #         print e.reason



if __name__ == '__main__':
    unittest.main()
