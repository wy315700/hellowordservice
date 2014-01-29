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


from loginHandler import LoginHandler
from registerHandler import RegisterHandler
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



class ChangeInfoHandler(tornado.web.RequestHandler):
	"""RequestHandler for Changing users' information"""
	def post(self):
		user_name = self.get_argument("userName")
		user_nickname = self.get_argument("userNickname")
		old_password = self.get_argument("oldPassword")
		new_password = self.get_argument("newPassword")
		#???users may change email???
		#user_email = self.get_argument("userEmail")
		#????????????????

		user_info = self.application.db.find({"name": user_name, "password": old_password})
		if user_info:
			self.application.db.modify({"name": user_name, "password": new_password, "nickname": user_nickname})
			return True
		else: 
			return False
		

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/user/register.json", RegisterHandler),
			(r"/user/login.json", LoginHandler),
			(r"/user/logout", LogoutHandler),
			(r"/user/change_userinfo", ChangeInfoHandler)
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
