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

import database.mysqlhelper as mysqlhelper


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
        userAvatarType = ''
        userAvatar = ''
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
            userAvatarType = params['userInfo']['userAvatarType']
            userAvatar     = params['userInfo']['userAvatar']
        except Exception, e:
            pass            

        try:
            user = mysqlhelper.UserInfo()
            user.setUserInfo(userName, userEmail, userNickname)
            user.setUserPassword(password)

            if userAvatarType != '':
                user.setUserAvatarInfo(userAvatarType,userAvatar)
            userID = user.saveUserInfo()
            if userID > 0:
                sessionID = str(uuid4())
                user.createSession(sessionID,userID)
                self.printSuccess(userID, user.userName, user.userNickname, user.userEmail,user.userAvatarType, user.userAvatar, sessionID)
                return
            else:
                raise Exception
        except Exception, e:
            self.printError('20101', 'register failed!')

            logging.warning(traceback.format_exc())

    def printSuccess(self,userID,userName,userNickname, userEmail, userAvatarType, userAvatar, sessionID):
        response = {
            "request" : "/user/register.json",
            "result"  : "success",
            "details" : {
                "userInfo":{
                    "userID" : userID,
                    "userName" : userName,
                    "userNickname" : userNickname,
                    "userEmail" : userEmail,
                    "userAvatarType" : userAvatarType,
                    "userAvatar" : userAvatar
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