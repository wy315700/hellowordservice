# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  LongPollDemo.py
#  helloword
#
#  Created by 汪 洋 on 14-2-9.
#  Copyright (c) 2014年 helloword. All rights reserved.
#

import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid
import traceback
import json

from tornado import gen

import sys
sys.path.append("./database/")
import mysqlhelper

class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cache_size = 200

    def wait_for_messages(self, callback, cursor=None):
        # if cursor:
        #     new_count = 0
        #     for msg in reversed(self.cache):
        #         if msg["id"] == cursor:
        #             break
        #         new_count += 1
        #     if new_count:
        #         callback(self.cache[-new_count:])
        #         return
        self.waiters.add(callback)

    def cancel_wait(self, callback):
        self.waiters.remove(callback)

    def new_messages(self, messages):
        logging.info("Sending new message to %r listeners", len(self.waiters))
        for callback in self.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        self.waiters = set()
        self.cache.extend(messages)
        if len(self.cache) > self.cache_size:
            self.cache = self.cache[-self.cache_size:]


# Making this a non-singleton is left as an exercise for the reader.
global_message_buffer = MessageBuffer()


class BaseHandler(tornado.web.RequestHandler):
    pass



class MessageUpdatesHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)

        if self.get_params() == -1:
            return

        global_message_buffer.wait_for_messages(self.on_new_messages,
                                                cursor=cursor, gameID=self.gameID)

    def on_new_messages(self, messages, success=False):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        if success:
            self.printSuccess()
        else:
            self.printError('20401', 'game error!')

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.on_new_messages)


    def get_user_by_sessions(self):
        try:
            user   = mysqlhelper.UserInfo()
            result = user.getUserIDBySession(self.sessionID)

            if result == 0:
                self.user = user
                return 0
                pass
            else:
                raise Exception 
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("20301", "session error")
            return -1
    
    def get_params(self):
        try:
            paramStr = self.get_argument("params");
            params = json.loads(paramStr);
            if params['request'] == "/helloword/game.json":
                self.sessionID = params['sessionID']
                self.gameID    = params['gameID']
                return 0
            else:
                raise Exception
        except Exception, e:
            logging.warning(traceback.format_exc())
            self.printError("10001", "params error")
            return -1

    def printSuccess(self):
        response = {
                    "request" : "/user/login.json",
                    "result": "success", 
                    "details": {
                        ## more info
                    }
                }
        self.write(json.dumps(response))
        self.finish()
    def printError(self,errorCode, error):
        response = {
                "request" : "/helloword/game.json",
                "result": "failed", 
                "details": {
                    "errorCode" : errorCode,
                    "error" : error
                }
            }
        logging.warning(traceback.format_exc())
        self.write(json.dumps(response))
        self.finish()




if __name__ == "__main__":
    pass
