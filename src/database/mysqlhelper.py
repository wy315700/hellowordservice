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
import random
import string
import hashlib
import uuid
import os
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
        self.salt     = ''
        self.userEmail= ''
        self.userAvatarType = 'id'
        self.userAvatar     = '1'
    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def setUserInfo(self, userName, userEmail, userNickname):
        self.userName = MySQLdb.escape_string(userName)
        self.userEmail= MySQLdb.escape_string(userEmail)
        self.userNickname= MySQLdb.escape_string(userNickname)

    def setUserSalt(self,salt):
        self.salt = salt

    def setUserAvatarInfo(self,avatarType,avatar):
        self.userAvatarType = MySQLdb.escape_string(avatarType)
        self.userAvatar     = MySQLdb.escape_string(avatar)
    
    def setUserPassword(self, plainPassword):
        if self.salt == '':
          self.createSalt()

        self.password = self.getHashedPassword(plainPassword, self.salt)
    def createSalt(self):
        self.salt = self.my_random_string(10)
    def getHashedPassword(self,password,salt):
      return hashlib.sha1(password.encode("utf-8") + salt).hexdigest()

    def varifyPassword(self, plainPassword):
        return self.getHashedPassword(plainPassword,self.salt) != self.password

    def my_random_string(self,string_length=10):
      """Returns a random string of length string_length."""
      random = str(uuid.uuid4()) # Convert uuid format to python string.
      random = random.lower() # Make all characters uppercase.
      random = random.replace("-","") # Remove the uuid '-'.
      return random[0:string_length] # Return the random string.
      # """using cryptographic safety random functions"""
      # return os.urandom(string_length)

    def saveUserInfo(self):
        sql = """INSERT INTO userinfo(userName,
         password, salt, userEmail, userNickname, userAvatarType, userAvatar)
         VALUES ('%s', '%s','%s', '%s', '%s', '%s', '%s')""" % (self.userName,self.password,self.salt, self.userEmail, self.userNickname, self.userAvatarType, self.userAvatar)
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
               logging.warning(traceback.format_exc())
               self.db.rollback()
               return -1

    def updateUserAvatar(self):
        sql = """update userinfo set 
         userAvatarType = '%s', userAvatar = '%s'
         where userName = '%s' """ % ( self.userAvatarType, self.userAvatar, self.userName)
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
            self.salt     = row['salt']
            self.userEmail= row['userEmail']
            self.userNickname = row['userNickname']
            self.userAvatarType = row['userAvatarType']
            self.userAvatar     = row['userAvatar']
            return 0
            # Now print fetched result
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
            print row
            self.userID   = row['userID']
            self.userName = row['userName']
            self.password = row['password']
            self.salt     = row['salt']
            self.userEmail= row['userEmail']
            self.userNickname = row['userNickname']
            self.userAvatarType = row['userAvatarType']
            self.userAvatar     = row['userAvatar']
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

    def getMaxAndMinRowNum(self,tableName, rowName):
      sql = "SELECT max(%s) as max , min(%s) as min FROM %s" %(rowName,rowName, tableName)
      self.cursor.execute(sql)
      # Fetch all the rows in a list of lists.
      results = self.cursor.fetchall()
      result = results[0]
      return result['max'],result['min']

    def getGame(self, gameType, num):
        if not gameType:
            """an error handle"""
            return -1
        if isinstance(gameType, long):
          gameType = str(gameType)
        gameType = MySQLdb.escape_string(gameType)
        tableList = {
          "1" : "exam_cet4_en2zh",
          "2" : "exam_cet4_zh2en",
          "3" : "exam_cet6_en2zh",
          "4" : "exam_cet6_zh2en",
          "5" : "exam_toefl_en2zh",
          "6" : "exam_toefl_zh2en",
          "7" : "exam_ielts_en2zh",
          "8" : "exam_ielts_zh2en",
          "9" : "exam_gre_en2zh",
          "10" : "exam_gre_zh2en",
        }
        if gameType not in ["1","2","3","4","5","6","7","8","9","10"]:
          return -1

        tableName = tableList[gameType]
        max,min = self.getMaxAndMinRowNum(tableName,"pro_id")


        sql =  "SELECT * FROM %s WHERE pro_id in (" %(tableName)

        b_list = range(min,max)
        
        rand_list = random.sample(b_list,num)

        for i in range(0,num):
          sql += str(rand_list[i])
          if i != 9:
            sql += ","

        # for i in range(0,num):
        #   sql += str(random.randint(min, max) )
        #   if i != 9:
        #     sql += ","

        sql += ")"

        logging.info(sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()

            return results
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