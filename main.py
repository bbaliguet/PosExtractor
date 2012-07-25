import webapp2, jinja2, os
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('Nothing here !')


class ConfHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			template = jinja_environment.get_template('templates/conf.html')
			self.response.out.write(template.render({}))
		else:
			self.redirect(users.create_login_url(self.request.uri))
	def post(self):
		pass


app = webapp2.WSGIApplication([('/', MainHandler), ('/conf', ConfHandler)], debug=True)
