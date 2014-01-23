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
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] != "/user/login.json":
                userName = params['loginInfo']['userName']


                password = params['loginInfo']['password']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.write("failed")
            return
        

        #=======================================
        user_info = self.application.db.find({"name": userName, "password": password})
        if user_info:
            sessionID = uuid4()
            self.write(user_info)

            #============there're some problems with the json data===============
            # self.write({
            #     "request" : "/user/login.json",
            #     "result": "success", 
            #     "details": {
            #         "userInfo": {
            #             "userID": "%d",
            #             "userName": "%f",
            #             "userNickname": "%f",
            #             "userEmail": "%f"
            #         },
            #         "sessionID": "%d"
            #     }} % (user_info[id], user_info[name], user_info[nickname], user_info[email], sessionID)
            # )
            #==================================================================
        else:
            self.write("failed")