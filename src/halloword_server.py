#created on Jan 23 2014 by LL
#modified on (please add modification date here)
#for our convenience, write comments for modification as detailed as possible
#this version is far from completion, a lot of work to update
#to do: add torndb module, add asyncronous for user actions (for database IO is time-consuming), 
#       fix the json transmission, add hash for password, add logs

import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import json

import logging
from uuid import uuid4

from tornado.options import define, options
define("port", default = 8000, help = "run on the given port",type = int)


from LoginHandler import LoginHandler
from RegisterHandler import RegisterHandler
from ChangeInfoHandler import ChangeInfoHandler
from Longpolldemo import MessageUpdatesHandler,MessageNewHandler
from GameHandler import RequestGameHandler, RequestRankHandler,UploadResultHandler,UserLogoutHandler,RequestPKGameHandler,UploadPKResultHandler

class Users(object):
	"""Handle with the users' operation"""
	session_queue = []
	callbacks = []
	def __init__(self, arg):
		super(Users, self).__init__()
		self.arg = arg
		
class MyDataBase(object):
	"""DOA of mysql database, hope I get DOA in the right way"""
	#=======temp data for test=========
	mydata = []
	#==================================
	def __init__(self):
		"""connection for the database"""
		self.mydata = [
			{"name": "aaa", "password": "aaaaaa", "id": "apple@aaa", "nickname": "apple", "email": "apple@aaa"},
			{"name": "bbb", "password": "bbbbbb", "id": "banana@bbb", "nickname": "banana", "email": "banana@bbb"},
			{"name": "ccc", "password": "cccccc", "id": "coco@ccc", "nickname": "coco", "email": "coco@ccc"}
		]
	def find(self, data_dict):
		for info in self.mydata:
			if info["name"] == data_dict["name"] and info["password"] == data_dict["password"]:
				return info
		return False
	def modify(self, data_dict):
		return True
	def add(self, data_dict):
		return True
	def remove(self, data_dict):
		return True
		




class LogoutHandler(tornado.web.RequestHandler):
	"""RequestHandler for logout"""
	def post(self):
		current_ssID = self.get_argument(sessionID)
		self.application.session_queue.remove(current_ssID)

		

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/user/register.json", RegisterHandler),
			(r"/user/login.json", LoginHandler),
			(r"/user/logout.json", LogoutHandler),
			(r"/user/change_userinfo.json", ChangeInfoHandler),
			(r"/helloword/request_game.json", RequestGameHandler),
			(r"/helloword/request_pk_game.json", RequestPKGameHandler),
			(r"/helloword/upload_pk_result.json", UploadPKResultHandler),
			(r"/helloword/upload_result.json", RequestRankHandler),
			(r"/helloword/request_rank.json", UploadResultHandler),
			(r"/helloword/user_logout.json", UserLogoutHandler),
			(r"/helloword/get_message.json", MessageUpdatesHandler),
			(r"/helloword/new_message.json", MessageNewHandler),
			
		]
		settings = {
			"template_path": "templates",
			"static_path": "static"
		}
		self.db = MyDataBase()
		#self.users = Users()
		tornado.web.Application.__init__(self, handlers, **settings)
		
if __name__ == "__main__":
	tornado.options.parse_command_line();
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
