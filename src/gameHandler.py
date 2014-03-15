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
import random
import copy

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
                # sessionID = params['sessionID']


                gameType = params['gameType']

        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return
        
        #=======================================
        try:
            user = mysqlhelper.UserInfo()

            # result = user.getUserIDBySession(sessionID)
            result = 0
            if result == 0:
                ## 产生题目

                pvpGameHander = mysqlhelper.PvpGameInfo()

                ans = pvpGameHander.getGame(gameType,"10")

                if ans != -1:

                    examList = []

                    for x in xrange(0,10):
                        moreAns = self.getRandomAns(ans)
                        examNode = {
                            "description":moreAns['pro_description'],
                            "ans1" : moreAns['pro_ans_a'],
                            "ans2" : moreAns['pro_ans_b'],
                            "ans3" : moreAns['pro_ans_c'],
                            "ans4" : moreAns['pro_ans_d'],
                            "point" : moreAns['pro_point'], #分值
                            "ans"   :  moreAns['pro_ans'],
                            "time"  : moreAns['pro_time'],
                            "enemyTime" : "3",
                            "enemyAns" : "a"
                        }
                        examList.append(examNode)


                    self.printSuccess(examList)

                return
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20101", "login failed")

    def getRandomAns(self,ans):
        alphaList = ['a','b','c','d']
        randomAnsList = copy.deepcopy(alphaList)
        random.shuffle(randomAnsList)
        result = copy.deepcopy(ans)
        
        for i in range(0,4):
            result['pro_ans_' + alphaList[i] ] = ans['pro_ans_' + randomAnsList[i] ]

            if randomAnsList[i] == alphaList[result['pro_ans']]:
                result['pro_ans'] = i

        return result




    def printSuccess(self,examList):
        response = {
                    "request" : "/helloword/request_pk_game.json",
                    "result"  : "success",
                    "details" : {
                        "num" : "10",
                        "gameID" : "1111",
                        "games" : examList
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