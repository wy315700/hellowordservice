# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  gameHandler.m
#  helloword
#
#  Created by 汪 洋 on 14-2-17.
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


class RequestGameHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/helloword/request_game.json",
        #"sessionID"  : "",
        #"gameType" : ""
        #}
        sessionID = ''
        gameType = ''
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/helloword/request_game.json":
                sessionID = params['sessionID']


                gameType = params['gameType']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(sessionID)
            if result == 0:
                ## 产生题目
                self.printSuccess()
                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def printSuccess(self):
        response = {
                    "request" : "/helloword/request_game.json",
                    "result"  : "success",
                    "details" : {
                        "num" : "10",
                        "gameID" : "",
                        "games" : [
                        {
                            "description":"aaa",
                            "ans1" : "1",
                            "ans2" : "2",
                            "ans3" : "3",
                            "ans4" : "4",
                            "point" : "5", #分值
                            "time"  : "5"
                        },
                        {
                            "description":"bbb",
                            "ans1" : "1",
                            "ans2" : "2",
                            "ans3" : "3",
                            "ans4" : "4",
                            "point" : "5", #分值
                            "time"  : "5"
                        }
                        ]
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


class UploadResultHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/helloword/upload_result.json",
        #"sessionID" : "",
        #"gameID"  : "",
        #"userAnswer":[
        #  {
        #    "chosen" : "a",
        #    "time"   : "5",
        #    },
        #  {
        #    //
        #  }
        #]
        #}
        sessionID = ''
        gameID = ''
        userAnswer = []
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/helloword/upload_result.json":
                sessionID = params['sessionID']


                gameType = params['gameType']

                userAnswer = params['userAnswer']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(sessionID)
            if result == 0:
                ## 存储答案
                self.printSuccess()
                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def printSuccess(self):
        response = {
            "request" : "/helloword/upload_result.json",
            "result"  : "success",
            "details" : {
                "correct" : "2",
                "incorrect" : "3",
                "thisScore" : "2",
                "totalScore" : "22",
                "userRank" : "23"
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


class RequestRankHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/helloword/request_rank.json",
        #"sessionID" : ""
        #}
        sessionID = ''
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/helloword/request_rank.json":
                sessionID = params['sessionID']


        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(sessionID)
            if result == 0:
                ## 获取积分
                self.printSuccess()
                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def printSuccess(self):
        response = {
            "request" : "/helloword/request_rank.json",
            "result"  : "success",
            "details" : {
                "totalScore" : "22",
                "userRank" : "23"
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


class UserLogoutHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/helloword/user_logout.json",
        #"sessionID" : "",
        #"gameID"  : "",
        #"logout"  : "true"
        #}
        sessionID = ''
        gameID = ''
        logout = False
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/helloword/user_logout.json":
                sessionID = params['sessionID']
                gameID = params['gameID']
                logout = params['logout']
                if logout != True:
                    raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(sessionID)
            if result == 0:
                ## 用户退出
                self.printSuccess()
                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def printSuccess(self):
        response = {
            "request" : "/helloword/user_logout.json",
            "result"  : "success"
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


class RequestPKGameHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/helloword/request_game.json",
        #"sessionID"  : "",
        #"gameType" : ""
        #}
        sessionID = ''
        gameType = ''
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/helloword/request_pk_game.json":
                sessionID = params['sessionID']


                gameType = params['gameType']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(sessionID)
            if result == 0:
                ## 产生题目
                self.printSuccess()
                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def printSuccess(self):
        response = {
                    "request" : "/helloword/request_pk_game.json",
                    "result"  : "success",
                    "details" : {
                        "num" : "10",
                        "gameID" : "",
                        "games" : [
                        {
                            "description":"aaa",
                            "ans1" : "1",
                            "ans2" : "2",
                            "ans3" : "3",
                            "ans4" : "4",
                            "point" : "5", #分值
                            "ans"   :  "a",
                            "time"  : "5",
                            "enemyTime" : "3",
                            "enemyAns" : "a"
                        },
                        {
                            "description":"bbb",
                            "ans1" : "1",
                            "ans2" : "2",
                            "ans3" : "3",
                            "ans4" : "4",
                            "point" : "5", #分值
                            "time"  : "5",
                            "ans"   :  "a",
                            "time"  : "5",
                            "enemyTime" : "3",
                            "enemyAns" : "a"
                        }
                        ]
                    } 
                }
        self.write(json.dumps(response))
    def printError(self,errorCode, error):
        response = {
                "request" : "/helloword/request_pk_game.json",
                "result": "failed", 
                "details": {
                    "errorCode" : errorCode,
                    "error" : error
                }
            }
        logging.warning(traceback.format_exc())
        self.write(json.dumps(response))



class UploadPKResultHandler(tornado.web.RequestHandler):
    """RequestHandler for login"""
    def post(self):
        #=======need further modification for json dict structure========
        #=======it is easy to test with current writing
        

        #{
        #"request" : "/helloword/upload_result.json",
        #"sessionID" : "",
        #"gameID"  : "",
        #"userAnswer":[
        #  {
        #    "chosen" : "a",
        #    "time"   : "5",
        #    },
        #  {
        #    //
        #  }
        #]
        #}
        sessionID = ''
        gameID = ''
        userAnswer = []
        try:
            paramStr = self.get_argument("params");

            params = json.loads(paramStr);
            if params['request'] == "/helloword/upload_pk_result.json":
                sessionID = params['sessionID']


                gameType = params['gameType']

                userAnswer = params['userAnswer']
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            result = user.getUserIDBySession(sessionID)
            if result == 0:
                ## 存储答案
                self.printSuccess()
                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def printSuccess(self):
        response = {
            "request" : "/helloword/upload_pk_result.json",
            "result"  : "success",
            "details" : {
                "correct" : "2",
                "incorrect" : "3",
                "totalExp" :"20",
                "userLevel" : "3"
            } 
        }
        self.write(json.dumps(response))
    def printError(self,errorCode, error):
        response = {
                "request" : "/helloword/upload_pk_result.json",
                "result": "failed", 
                "details": {
                    "errorCode" : errorCode,
                    "error" : error
                }
            }
        logging.warning(traceback.format_exc())
        self.write(json.dumps(response))