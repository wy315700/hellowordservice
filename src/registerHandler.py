# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  registerHandler.m
#  helloword
#
#  Created by 汪 洋 on 14-1-28.
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


class RegisterHandler(tornado.web.RequestHandler):
    """RequestHandler for register"""
    def post(self):

    #    {
    #  "request" : "/user/register.json",
    #  "userInfo" : {
    #    "userName" : "userName",
    #    "userNickname" : "userNickname",
    #    "password" : "password"
    #  }
    #}
        userName = ''
        password = ''
        userNickname = ''
        userEmail = ''
        try:
            paramStr = self.get_argument("params");
            params = json.loads(paramStr);
            if params['request'] == "/user/register.json":
                userName = params['userInfo']['userName']


                password = params['userInfo']['password']

                userNickname = params['userInfo']['userNickname']

                
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError('10001', 'params error!')
            return
        try:
            userEmail = params['userInfo']['userEmail']
        except Exception, e:
            userEmail = userName
            

        try:
            user = mysqlhelper.UserInfo()
            salt = user.my_random_string(10)

            password = user.getHashedPassword(password,salt)
            user.setUserInfo(userName, password, salt, userEmail, userNickname)
            userID = user.saveUserInfo()
            if userID > 0:
                sessionID = str(uuid4())
                user.createSession(sessionID,userID)
                self.printSuccess(userID, user.userName, user.userNickname, user.userEmail, sessionID)
                return
            else:
                raise Exception
        except Exception, e:
            self.printError('20101', 'register failed!')

            logging.warning(traceback.format_exc())

    def printSuccess(self,userID,userName,userNickname, userEmail, sessionID):
        response = {
            "request" : "/user/register.json",
            "result"  : "success",
            "details" : {
                "userInfo":{
                    "userID" : userID,
                    "userName" : userName,
                    "userNickname" : userNickname,
                    "userEmail" : userEmail
                    },
                    "sessionID" : sessionID
                } 
            }
        self.write(json.dumps(response))

    def printError(self,errorCode, error):
        response = {
                "request" : "/user/login.json",
                "result": "failed", 
                "details": {
                    "errorCode" : errorCode,
                    "error" : error
                }
            }
        logging.warning(traceback.format_exc())
        self.write(json.dumps(response))