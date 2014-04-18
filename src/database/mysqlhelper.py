# -*- coding: utf-8 -*-  
__author__ = 'wangyang'
#  mysqlhelper.m
#  helloword
#
#  Created by 汪 洋 on 14-1-25.
#  Copyright (c) 2014年 helloword. All rights reserved.
#
import MySQLdb

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.types import CHAR, Integer, String, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, or_, not_



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

##sqlalchemy 基本变量
global_engine = create_engine('mysql://root:asdfghjkl@localhost/helloword?charset=utf8')
BaseModel = declarative_base()
DB_Session = sessionmaker(bind=global_engine)
global_session = DB_Session()

class UserModel(BaseModel):
    __tablename__ = 'userinfo'

    userID = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(32))
    password = Column(String(40))
    salt = Column(String(10))
    userEmail = Column(VARCHAR(100))
    userNickname = Column(CHAR(32))
    userAvatarType = Column(CHAR(4))
    userAvatar = Column(VARCHAR(100))

class UserSessionModel(BaseModel):
    __tablename__ = 'sessions'

    sessionID = Column(CHAR(36), unique=True, primary_key=True)
    userID = Column(Integer)
    createTime = Column(TIMESTAMP,server_default = sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))

# class BaseExamModel(BaseModel):
#   __tablename__ = 'exam_list'
#   pro_id = Column(Integer, primary_key=True, autoincrement=True)
#   pro_description = Column(VARCHAR(50))
#   pro_ans_a = Column(VARCHAR(10))
#   pro_ans_b = Column(VARCHAR(10))
#   pro_ans_c = Column(VARCHAR(10))
#   pro_ans_d = Column(VARCHAR(10))
#   pro_point = Column(TINYINT(4))
#   pro_time = Column(TINYINT(4))
#   pro_type = Column(TINYINT(4))

class Cet4ExamModel(BaseModel):
  __tablename__ = 'exam_cet4'
  pro_id = Column(Integer, primary_key=True, autoincrement=True)
  pro_description = Column(VARCHAR(50))
  pro_ans_a = Column(VARCHAR(10))
  pro_ans_b = Column(VARCHAR(10))
  pro_ans_c = Column(VARCHAR(10))
  pro_ans_d = Column(VARCHAR(10))
  pro_point = Column(TINYINT(4))
  pro_time = Column(TINYINT(4))
  pro_type = Column(TINYINT(4))

class Cet6ExamModel(BaseModel):
  __tablename__ = 'exam_cet6'
  pro_id = Column(Integer, primary_key=True, autoincrement=True)
  pro_description = Column(VARCHAR(50))
  pro_ans_a = Column(VARCHAR(10))
  pro_ans_b = Column(VARCHAR(10))
  pro_ans_c = Column(VARCHAR(10))
  pro_ans_d = Column(VARCHAR(10))
  pro_point = Column(TINYINT(4))
  pro_time = Column(TINYINT(4))
  pro_type = Column(TINYINT(4))

class GreExamModel(BaseModel):
  __tablename__ = 'exam_gre'
  pro_id = Column(Integer, primary_key=True, autoincrement=True)
  pro_description = Column(VARCHAR(50))
  pro_ans_a = Column(VARCHAR(10))
  pro_ans_b = Column(VARCHAR(10))
  pro_ans_c = Column(VARCHAR(10))
  pro_ans_d = Column(VARCHAR(10))
  pro_point = Column(TINYINT(4))
  pro_time = Column(TINYINT(4))
  pro_type = Column(TINYINT(4))

class IeltsExamModel(BaseModel):
  __tablename__ = 'exam_ielts'
  pro_id = Column(Integer, primary_key=True, autoincrement=True)
  pro_description = Column(VARCHAR(50))
  pro_ans_a = Column(VARCHAR(10))
  pro_ans_b = Column(VARCHAR(10))
  pro_ans_c = Column(VARCHAR(10))
  pro_ans_d = Column(VARCHAR(10))
  pro_point = Column(TINYINT(4))
  pro_time = Column(TINYINT(4))
  pro_type = Column(TINYINT(4))

class ToeflExamModel(BaseModel):
  __tablename__ = 'exam_toefl'
  pro_id = Column(Integer, primary_key=True, autoincrement=True)
  pro_description = Column(VARCHAR(50))
  pro_ans_a = Column(VARCHAR(10))
  pro_ans_b = Column(VARCHAR(10))
  pro_ans_c = Column(VARCHAR(10))
  pro_ans_d = Column(VARCHAR(10))
  pro_point = Column(TINYINT(4))
  pro_time = Column(TINYINT(4))
  pro_type = Column(TINYINT(4))

class UserInfo():
    def __init__(self):
        """connection for the database"""
        if isSae:
          self.db = MySQLdb.connect(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_DB,3307,charset='utf8')
        else:
          self.db = MySQLdb.connect("localhost","root","asdfghjkl","helloword",charset='utf8' )
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        
        self._user = UserModel()
        self._session = DB_Session()
        self._user.userAvatarType='id'
        self._user.userAvatar='1'

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def setUserInfo(self, userName, userEmail, userNickname):
      if userName:
        self._user.userName = userName
      if userEmail:
        self._user.userEmail= userEmail
      if userNickname:
        self._user.userNickname= userNickname

    def setUserSalt(self,salt):
        self._user.salt = salt

    def setUserAvatarInfo(self,avatarType,avatar):
      if avatarType:
        self._user.userAvatarType = avatarType
      if avatar:
        self._user.userAvatar     = avatar
    
    def setUserPassword(self, plainPassword):
        if self._user.salt == '':
          self.createSalt()

        if self._user.salt is None:
          self.createSalt()

        self._user.password = self.getHashedPassword(plainPassword, self._user.salt)
        
    def createSalt(self):
        self.setUserSalt(self.my_random_string(10))

    def getHashedPassword(self,password,salt):
      return hashlib.sha1(password.encode("utf-8") + salt).hexdigest()

    def varifyPassword(self, plainPassword):
        return self.getHashedPassword(plainPassword,self._user.salt) == self._user.password

    def my_random_string(self,string_length=10):
      """Returns a random string of length string_length."""
      random = str(uuid.uuid4()) # Convert uuid format to python string.
      random = random.lower() # Make all characters uppercase.
      random = random.replace("-","") # Remove the uuid '-'.
      return random[0:string_length] # Return the random string.
      # """using cryptographic safety random functions"""
      # return os.urandom(string_length)

    def saveUserInfo(self):
      """using orm"""
      try:
        self._session.add(self._user)
        self._session.commit()
        return self._user.userID
      except Exception, e:
        logging.warning(traceback.format_exc())
        self._session.rollback()
        return -1

    def updateUserAvatar(self):
      """using orm"""
      try:
        query = self._session.query(UserModel).filter(UserModel.userName == self._user.userName)
        query.update({
            UserModel.userAvatarType : self._user.userAvatarType,
            UserModel.userAvatar : self._user.userAvatar
          })
        self._session.commit()
        return 0
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1

    def updateUserInfo(self):
      """using orm"""
      try:
        query = self._session.query(UserModel).filter(UserModel.userName == self._user.userName)
        query.update({
            UserModel.password : self._user.password,
            UserModel.userNickname : self._user.userNickname
          })
        self._session.commit()
        return 0
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1

    def getUserInfoByName(self, userName):
      """using orm"""
      try:
        query = self._session.query(UserModel).filter(UserModel.userName == userName)
        user = query.first()

        if user is None:
          raise Exception

        self._user = user
        return 0
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1


    def getUserInfoByID(self, userID):
      """using orm"""
      try:
        query = self._session.query(UserModel).filter(UserModel.userID == userID)
        
        user = query.first()
        if user is None:
          raise Exception

        self._user = user

        return 0
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1

    def getUserInfoBySessionID(self, sessionID):
      """using orm"""
      try:
        userID = self.getUserIDBySession(sessionID)
        return self.getUserInfoByID(userID)
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1


    def getUserIDBySession(self, sessionID):
      """using orm"""
      try:
        query = self._session.query(UserSessionModel).filter(UserSessionModel.sessionID == sessionID)
        
        userSession = query.first()

        if userSession is None:
          raise Exception


        return userSession.userID
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1

    def deleteSessionByUserID(self, userID):
      """using orm"""
      try:
        query = self._session.query(UserSessionModel).filter(UserSessionModel.userID == userID)
        query.delete()
        return 0
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1
    def deleteSessionBySessionID(self, sessionID):
      """using orm"""
      try:
        query = self._session.query(UserSessionModel).filter(UserSessionModel.sessionID == sessionID)
        query.delete()
        return 0
      except Exception, e:
        logging.warning(traceback.format_exc())
        return -1

    def createSession(self, sessionID, userID):
      """using orm"""
      if sessionID == '' or sessionID is None or userID is None or userID == 0:
        return -1

      userSession = UserSessionModel(sessionID = sessionID, userID = userID)

      try:
        self._session.add(userSession)
        self._session.commit()
      except Exception, e:
        logging.warning(traceback.format_exc())
        self._session.rollback()
    

class PvpGameInfo():
    def __init__(self, user = None):
        """connection for the database"""
        if isSae:
          self.db = MySQLdb.connect(sae.const.MYSQL_HOST,sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_DB,3307,charset='utf8')
        else:
          self.db = MySQLdb.connect("localhost","root","asdfghjkl","helloword",charset='utf8')
        self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
        self.cursor.execute("set names utf8")
        self._user = user
        self._session = DB_Session()


    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()


    def getMaxAndMinRowNum(self,tableName, rowName):
      sql = "SELECT max(%s) as max , min(%s) as min FROM %s" %(rowName,rowName, tableName)
      try:
        return self._session.execute(sql).first()
      except Exception, e:
        logging.warning(traceback.format_exc())

    def getGame(self, gameType, num):
        if not gameType:
            """an error handle"""
            return -1
        if isinstance(gameType, long):
          gameType = str(gameType)

        tableList = {
          "1" : "exam_cet4",
          "3" : "exam_cet6",
          "5" : "exam_toefl",
          "7" : "exam_ielts",
          "9" : "exam_gre",
        }

        modelList = {
          "1" : Cet4ExamModel,
          "3" : Cet6ExamModel,
          "5" : ToeflExamModel,
          "7" : IeltsExamModel,
          "9" : GreExamModel,
        }
        if gameType not in ["1","2","3","4","5","6","7","8","9","10"]:
          return -1

        tableName = tableList[gameType]

        modelClass = modelList[gameType]

        max,min = self.getMaxAndMinRowNum(tableName,"pro_id")

        b_list = range(min,max)
        
        rand_list = random.sample(b_list,num)

        try:
            # Execute the SQL command
            query = self._session.query(modelClass).filter(modelClass.pro_id.in_(rand_list))
            # Fetch all the rows in a list of lists.
            l = query.all()
            results = []

            row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}

            for row in l:
              results.append(row2dict(row))
            # self.saveGameListToCache(self.user.userID, gameType, rand_list)
            return results
        except:
            print "Error: unable to fecth data"
            logging.warning(traceback.format_exc())
            # Rollback in case there is any error
            self.db.rollback()
            return -1

    def saveGameListToCache(self,userID,gameType,gameList):
      if not userID or not gameList:
        return -1
      if not isinstance(gameList,list):
        return -1
      if len(gameList) == 0:
        return -1;
      
      sql = "INSERT INTO `user_pk_game_cache` (`userID`,`userGameType`,`userGameIDs`) VALUES (%d,'%s','%s')" %(userID,gameType,repr(gameList) )

      try:
        # Execute the SQL command
        self.cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        return 0
      except:
        print "Error: unable to fecth data"
        logging.warning(traceback.format_exc())
        # Rollback in case there is any error
        self.db.rollback()
        return -1


        
if __name__ == "__main__":
  # BaseModel.metadata.create_all(global_engine)
  # user = UserModel(userName="12a'2",password='111',salt='12')
  # global_session.add(user)
  # user.userName = '11'
  # global_session.commit()
  sql = "SELECT max(`pro_id`) as max , min(`pro_id`) as min FROM `exam_cet4_en2zh`"
  print global_session.execute(sql).first()
  pass