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

try:
  import sae
  isSae = True
except Exception, e:
  isSae = False

        
class UserInfo():
    def __init__(self):
        """connection for the database"""
        if isSae:
          self.db = MySQLdb.connect(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_DB,3307,charset='utf8')
        else:
          self.db = MySQLdb.connect("localhost","root","asdfghjkl","helloword",charset='utf8' )
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

    def updateUserInfo(self):
        sql = """update userinfo set 
         password = '%s', userNickname = '%s'
         where userName = '%s' """ % (self.password, self.userNickname, self.userName)
        logging.debug(sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            num = self.db.affected_rows()
            if num != 1:
                raise Exception
            self.db.commit()
            return 0
        except:
            # Rollback in case there is any error
            logging.warning(traceback.format_exc())
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

    def getUserInfoByID(self, userID):
        if not userID:
            """an error handle"""
            return -1
        if isinstance(userID, long):
          userID = str(userID)
        userID = MySQLdb.escape_string(userID)
        sql =  "SELECT * FROM userinfo \
                WHERE userID = '%s'" % (userID)
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

    def getUserIDBySession(self, sessionID):
        sessionID = MySQLdb.escape_string(sessionID)

        sql =  "SELECT * FROM sessions \
                WHERE sessionID = '%s'" % (sessionID)
        logging.debug(sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
            if len(results) == 0 :
                raise Exception

            row = results[0]
            self.userID   = row['userID']
            self.getUserInfoByID(self.userID)
            # Now print fetched result
            return 0
        except:
            print "Error: unable to fecth data"
            logging.warning(traceback.format_exc())
            # Rollback in case there is any error
            self.db.rollback()
            return -1

    def deleteSessionByUserID(self, userID):
        sql = "DELETE FROM sessions WHERE userID='%s'" % (userID)

        logging.debug(sql)
        try:
               # Execute the SQL command
               self.cursor.execute(sql)
               # Commit your changes in the database
               self.db.commit()
               return 0
        except:
               # Rollback in case there is any error
               logging.warning(traceback.format_exc())
               self.db.rollback()
               return -1
    def deleteSessionBySessionID(self, sessionID):
        sql = "DELETE FROM sessions WHERE sessionID='%s'" % (sessionID)

        logging.debug(sql)
        try:
               # Execute the SQL command
               self.cursor.execute(sql)
               # Commit your changes in the database
               self.db.commit()
               return 0
        except:
               # Rollback in case there is any error
               logging.warning(traceback.format_exc())
               self.db.rollback()
               return -1

    def createSession(self, sessionID, userID):
        sql = """INSERT INTO sessions(sessionID,
         userID) VALUES ('%s', '%s')""" % (sessionID,userID)
        logging.debug(sql)
        try:
               # Execute the SQL command
               self.cursor.execute(sql)
               # Commit your changes in the database
               self.db.commit()
               return 0
        except:
               # Rollback in case there is any error
               logging.warning(traceback.format_exc())
               self.db.rollback()
               return -1
    

class PvpGameInfo():
    def __init__(self):
        """connection for the database"""
        if isSae:
          self.db = MySQLdb.connect(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_DB,3307,charset='utf8')
        else:
          self.db = MySQLdb.connect("localhost","root","asdfghjkl","helloword",charset='utf8')
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute("set names utf8")

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def getGame(self, gameType, num):
        if not gameType:
            """an error handle"""
            return -1
        if isinstance(gameType, long):
          gameType = str(gameType)
        gameType = MySQLdb.escape_string(gameType)
        sql =  "SELECT * FROM test_exam LIMIT 0,1"
        logging.info(sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()

            row = results[0]
            
            print row

            return row
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