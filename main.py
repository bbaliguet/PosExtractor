import webapp2, jinja2, os
from google.appengine.api import users
from handlers import conf, extract, alltrack


class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.status = 417


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/conf', conf.ConfHandler),
	('/all', alltrack.AllHandler),	
	('/_extract', extract.ExtractHandler)],
	debug=True)
