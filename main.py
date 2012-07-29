import webapp2, jinja2, os
from google.appengine.api import users
from handlers import conf


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('Nothing here !')


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/conf', conf.ConfHandler)],
	debug=True)
