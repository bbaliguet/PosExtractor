import webapp2, jinja2, os
from google.appengine.api import users
from handlers import conf, extract


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.status = 417


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/conf', conf.ConfHandler),
	('/_extract', extract.ExtractHandler)],
	debug=True)
