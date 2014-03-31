# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  ChangeHandler.m
#  helloword
#
#  Created by 汪 洋 on 14-2-2.
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



class ChangeInfoHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/user/change_userinfo.json",
        #"sessionID" : "sessionID"
        #"userInfo" : {
        #    "userName" : "userName",
        #    "userNickname" : "userNickname",
        #    "oldPassword" : "oldPassword"
        #    "newPassword" : "newPassword"
        #    }
        #}
        userName     = ''
        userNickname = ''
        oldPassword  = ''
        newPassword  = ''
        userEmail    = ''

        userSession  = ''
        try:
            paramStr = self.get_argument("params")

            params = json.loads(paramStr)
            if params['request'] == "/user/change_userinfo.json":
                userSession  = params['sessionID']
                userName     = params['userInfo']['userName']
                userNickname = params['userInfo']['userNickname']
                oldPassword  = params['userInfo']['oldPassword']
                newPassword  = params['userInfo']['newPassword']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(userSession)
            if result == 0:
                if oldPassword != user.password:
                    raise Exception
                user.setUserInfo(userName, newPassword, userEmail, userNickname)
                result = user.updateUserInfo()
                if result == 0:
                    #sessionID = str(uuid4())
                    self.printSuccess(user.userID, user.userName, user.userNickname, user.userEmail)
                    return
                else:
                    raise Exception
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20201", "change userInfo failed")

    def printSuccess(self,userID,userName,userNickname, userEmail):
        response = {
                    "request" : "/user/change_userinfo.json",
                    "result": "success", 
                    "details": {
                        "userInfo": {
                            "userID": userID,
                            "userName": userName,
                            "userNickname": userNickname,
                            "userEmail": userEmail
                        }
                    }
                }
        self.write(json.dumps(response))
    def printError(self,errorCode, error):
        response = {
                "request" : "/user/change_userinfo.json",
                "result": "failed", 
                "details": {
                    "errorCode" : errorCode,
                    "error" : error
                }
            }
        logging.warning(traceback.format_exc())
        self.write(json.dumps(response))