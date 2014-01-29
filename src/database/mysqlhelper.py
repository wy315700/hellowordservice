# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  mysqlhelper.m
#  helloword
#
#  Created by 汪 洋 on 14-1-25.
#  Copyright (c) 2014年 helloword. All rights reserved.
#
import MySQLdb

import logging
import traceback
from uuid import uuid4



        
class UserInfo():
    def __init__(self):
        """connection for the database"""
        self.db = MySQLdb.connect("localhost","root","asdfghjkl","helloword" )
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        self.userName = ''
        self.password = ''
        self.userEmail= ''
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def setUserInfo(self, userName, password, userEmail, userNickname):
        self.userName = MySQLdb.escape_string(userName)
        self.password = MySQLdb.escape_string(password)
        self.userEmail= MySQLdb.escape_string(userEmail)
        self.userNickname= MySQLdb.escape_string(userNickname)
    
    def saveUserInfo(self):
        sql = """INSERT INTO userinfo(userName,
         password, userEmail, userNickname)
         VALUES ('%s', '%s', '%s', '%s')""" % (self.userName,self.password, self.userEmail, self.userNickname)
        logging.debug(sql)
        try:
               # Execute the SQL command
               self.cursor.execute(sql)
               # Commit your changes in the database
               userID = self.db.insert_id()
               self.db.commit()
               return userID
        except:
               # Rollback in case there is any error
               self.db.rollback()
               return -1

    def getUserInfoByName(self, userName):
        if not userName:
            """an error handle"""
            return -1
        userName = MySQLdb.escape_string(userName)
       	sql =  "SELECT * FROM userinfo \
                WHERE userName = '%s'" % (userName)
        logging.debug(sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            if len(results) != 1:
                raise Exception

            row = results[0]
            self.userID   = row['userID']
            self.userName = row['userName']
            self.password = row['password']
            self.userEmail= row['userEmail']
            self.userNickname = row['userNickname']
            # Now print fetched result
            logging.debug("userName=%s,password=%s,userEmail=%s" % \
            (self.userName, self.password, self.userEmail) )
            return 0
        except:
            print "Error: unable to fecth data"
            logging.warning(traceback.format_exc())
            # Rollback in case there is any error
            self.db.rollback()
            return -1

        




        
if __name__ == "__main__":
	user = UserInfo()
	result = user.getUserInfoByName("aa")
	pass