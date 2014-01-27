# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  databaseTest.m
#  helloword
#
#  Created by 汪 洋 on 14-1-24.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import unittest
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
        
    


if __name__ == '__main__':
    unittest.main()
