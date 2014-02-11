# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  databaseTest.m
#  helloword
#
#  Created by 汪 洋 on 14-1-24.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import unittest
import uuid
import sys
sys.path.append("../database/")

import mysqlhelper

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.user = mysqlhelper.UserInfo()

    def test_get_user_success(self):

        result = self.user.getUserInfoByName("aaa")
        self.assertEqual(result,0)
        self.assertEqual('aaaaaa',self.user.password)

    def test_get_user_failed(self):

        result = self.user.getUserInfoByName("bb")
        self.assertEqual(result,-1)

    def test_get_user_by_id(self):

        result = self.user.getUserInfoByID("1")
        self.assertEqual(result,0)
        self.assertEqual('aaaaaa',self.user.password)

    def test_save_user(self):

        self.user.setUserInfo("1", "2", "3", "4")
        result = self.user.saveUserInfo()
        self.assertNotEqual(result,-1)
    
    def test_update_user(self):

        self.user.setUserInfo("1", "22", "33", "44")
        result = self.user.updateUserInfo()
        self.assertNotEqual(result,-1)

    def test_create_session(self):
        result = self.user.createSession(str(uuid.uuid4()),'1')
        self.assertNotEqual(result,-1)
    
    def test_delete_session_by_user_id(self):
        #result = self.user.deleteSessionByUserID('1')
        #self.assertNotEqual(result,-1)
        pass

    def test_delete_session_by_session_id(self):
        result = self.user.deleteSessionBySessionID('4eea99eb-74ed-4df8-923d-5f39da27d87c')
        self.assertNotEqual(result,-1)

    def test_get_user_by_session_id(self):
        result = self.user.getUserIDBySession('a0719d11-12b3-4878-8fcb-e13f4c6de35b')
        self.assertNotEqual(result,-1)
        pass

if __name__ == '__main__':
    unittest.main()
