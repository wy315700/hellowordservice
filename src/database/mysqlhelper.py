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
from sqlalchemy import desc
from sqlalchemy.types import CHAR, Integer, String, VARCHAR, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT,INTEGER

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound



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
if isSae:
  global_engine = create_engine('mysql://%s:%s@%s:%d/%s?charset=utf8' % (sae.const.MYSQL_USER,sae.const.MYSQL_PASS,sae.const.MYSQL_HOST,3307,sae.const.MYSQL_DB) , encoding='utf8', pool_recycle=10 )
else:
  global_engine = create_engine('mysql://root:asdfghjkl@localhost/helloword?charset=utf8',echo=False)
BaseModel = declarative_base()
DB_Session = sessionmaker(bind=global_engine)
global_session = DB_Session()

class UserModel(BaseModel):
    __tablename__ = 'userinfo'

    userID = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
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
    userID = Column(INTEGER(10,unsigned=True))
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
  pro_id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
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
  pro_id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
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
  pro_id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
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
  pro_id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
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
  pro_id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
  pro_description = Column(VARCHAR(50))
  pro_ans_a = Column(VARCHAR(10))
  pro_ans_b = Column(VARCHAR(10))
  pro_ans_c = Column(VARCHAR(10))
  pro_ans_d = Column(VARCHAR(10))
  pro_point = Column(TINYINT(4))
  pro_time = Column(TINYINT(4))
  pro_type = Column(TINYINT(4))


class UserPkGameAnsModel(BaseModel):
  __tablename__ = 'user_pk_game_ans'
  ans_id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
  game_type = Column(TINYINT(4))
  pro_id = Column(INTEGER(10,unsigned=True))
  user_ans = Column(VARCHAR(20))

class UserPkGameCacheModel(BaseModel):
  __tablename__ = 'user_pk_game_cache'
  id = Column(INTEGER(10,unsigned=True), primary_key=True, autoincrement=True)
  userID = Column(INTEGER(10,unsigned=True), unique=True)
  userGameType = Column(TINYINT(4))
  userGameIDs = Column(String(100))
  createTime = Column(TIMESTAMP,server_default = sqlalchemy.sql.expression.text('CURRENT_TIMESTAMP()'))

class UserRankInfoModel(BaseModel):
  __tablename__ = 'user_rank_info'
  userID = Column(INTEGER(10,unsigned=True), primary_key=True)
  userScore = Column(INTEGER(10,unsigned=True))
  userExp = Column(INTEGER(10,unsigned=True))

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
        self.__row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}

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

            

            for row in l:
              results.append(self.__row2dict(row))
            self.saveGameListToCache(self._user.userID, gameType, rand_list)
            return results
        except:
            print "Error: unable to fecth data"
            logging.warning(traceback.format_exc())
            # Rollback in case there is any error
            self.db.rollback()
            return -1
    def varifyUserAns(self,userID,userAnsList):
      gameType , gameList = self.getGameListFromCache(userID)

      if gameList == -1:
        return -1

      #把用户做过的答案保存到题库里
      self.saveAIAns(gameType, gameList, userAnsList)

      modelList = {
          "1" : Cet4ExamModel,
          "3" : Cet6ExamModel,
          "5" : ToeflExamModel,
          "7" : IeltsExamModel,
          "9" : GreExamModel,
        }

      modelClass = modelList[gameType]

      query = self._session.query(modelClass).filter(modelClass.pro_id.in_(gameList))
      l = query.all()

      results = []
      for row in l:
        results.append(self.__row2dict(row))

      if len(userAnsList) != len(gameList):
        return -1

      thisScore = 0
      correctNum = 0
      incorrectNum = 0
      ##计算用户对了几个
      for i in range(len(userAnsList)):
        if userAnsList[i] == results[i]['pro_ans_a']:
          correctNum += 1
          thisScore += results[i]['pro_point']
        else:
          incorrectNum += 1

      try:
        query = self._session.query(UserRankInfoModel).filter(UserRankInfoModel.userID == userID)

        userRankInfoObj = query.one()
        #如果用户还没做过题，那么创建一个
      except NoResultFound, e:
        userRankInfoObj = UserRankInfoModel(userID = userID, userScore = 0, userExp = 0)
        self._session.add(userRankInfoObj)
        self._session.flush()
      except Exception,e:
        return -1
      
      userRankInfoObj.userScore += thisScore

      userRankInfoObj.userExp   += len(gameList)

      userScore = userRankInfoObj.userScore
      userExp   = userRankInfoObj.userExp
      self._session.commit()


      return {
        "correct" : correctNum,
        "incorrect" : incorrectNum,
        "userExp" : userExp,
        "userScore" : userScore
      }

    def getUserRank(self):
      try:
        self._getTopRank()
        thisUserRank = self._session.query(UserRankInfoModel).get(self._user.userID)

        if thisUserRank == None:
          return {
              "totalScore" : 0,
              "userRank" : 0
              }
        
        query = self._session.query(UserRankInfoModel).filter(UserRankInfoModel.userScore > thisUserRank.userScore)

        rank = query.count() + 1

        return {
          "totalScore" : thisUserRank.userScore,
          "userRank" : rank
        }

      except Exception, e:
        raise e

    def _getTopRank(self):
      try:
        query = self._session.query(UserRankInfoModel,UserModel).outerjoin(UserModel, UserModel.userID == UserRankInfoModel.userID).order_by(desc(UserRankInfoModel.userScore) ).limit(5)

        topRankList = query.all()

        for x in topRankList:
          print x[1].userNickname


      except Exception, e:
        raise e

    def getGameListFromCache(self,userID):
      try:
        query = self._session.query(UserPkGameCacheModel).filter(UserPkGameCacheModel.userID == userID)

        cache = query.one()

        gameType = str(cache.userGameType)

        gameList = cache.userGameIDs

        gameList = eval(gameList)
        
        return gameType,gameList
      except Exception, e:
        return (-1,-1)
      
    def saveAIAns(self,gameType, pro_id_list, ans_list):
      if not gameType or not pro_id_list or not ans_list:
        return -1;

      if not isinstance(pro_id_list,list) or not isinstance(ans_list, list):
        return -1;

      if len(pro_id_list) != len(ans_list):
        return -1;

      for i in xrange(len(pro_id_list)):
        ans = UserPkGameAnsModel(game_type = gameType,pro_id = pro_id_list[i],user_ans = ans_list[i])
        try:
          self._session.add(ans)
        except Exception, e:
          break
          return -1

      self._session.commit()
      return 0;

    def saveGameListToCache(self,userID,gameType,gameList):
      if not userID or not gameList:
        return -1
      if not isinstance(gameList,list):
        return -1
      if len(gameList) == 0:
        return -1;
      
      # sql = "INSERT INTO `user_pk_game_cache` (`userID`,`userGameType`,`userGameIDs`) VALUES (%d,'%s','%s')" %(userID,gameType,repr(gameList) )
      gameCache = UserPkGameCacheModel(userID = userID, userGameType = gameType, userGameIDs = repr(gameList))
      try:
        # Execute the SQL command
        self._session.add(gameCache)
        self._session.commit()
        # Fetch all the rows in a list of lists.
        return 0
      except IntegrityError,e:
        logging.warning("exists")
        self._session.rollback()
        # Rollback in case there is any error
        self._session.query(UserPkGameCacheModel).filter(UserPkGameCacheModel.userID == userID).delete()
        self._session.add(gameCache)
        self._session.commit()
        return 0
      except Exception,e:
        self._session.rollback()
        # Rollback in case there is any error
        return -1


        
if __name__ == "__main__":
  BaseModel.metadata.create_all(global_engine)
  # user = UserModel(userName="12a'2",password='111',salt='12')
  # global_session.add(user)
  # user.userName = '11'
  # global_session.commit()
  # sql = "SELECT max(`pro_id`) as max , min(`pro_id`) as min FROM `exam_cet4_en2zh`"
  # print global_session.execute(sql).first()
  pass