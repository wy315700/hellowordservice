# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  LoginHandler.m
#  helloword
#
#  Created by 汪 洋 on 14-1-23.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import json

import logging
import traceback
from uuid import uuid4

import sys
sys.path.append("./database/")
import mysqlhelper


class Users(object):
	"""Handle with the users' operation"""
	session_queue = []
	callbacks = []
	def __init__(self, arg):
		super(Users, self).__init__()
		self.arg = arg

class LoginHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #===============================
        #   {
        #        "request" : "/user/login.json",
        #        "loginInfo" : {
        #            "userName" : "userName",
        #            "password" : "password"
        #        }
        #    }
        userName = ''
        password = ''
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/user/login.json":
                userName = params['loginInfo']['userName']


                password = params['loginInfo']['password']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.write("failed")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserInfoByName(userName)
            if result == 0:
                if password != user.password:
                    raise Exception
                sessionID = str(uuid4())
                response = {
                    "request" : "/user/login.json",
                    "result": "success", 
                    "details": {
                        "userInfo": {
                            "userID": user.userID,
                            "userName": user.userName,
                            "userNickname": user.userNickname,
                            "userEmail": user.userEmail
                        },
                        "sessionID": sessionID
                    }
                }
                self.write(json.dumps(response))
                return
            else:
                raise Exception
        except Exception, e:
            response = {
                "request" : "/user/login.json",
                "result": "failed", 
                "details": {
                    "errorCode" : "20001",
                    "error" : "login failed"
                }
            }
            logging.warning(traceback.format_exc())
            self.write(json.dumps(response))