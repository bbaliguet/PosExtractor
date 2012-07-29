import webapp2, jinja2, os
from google.appengine.api import users
from livetrack import models

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class ConfHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			template = jinja_environment.get_template('templates/conf.html')
			self.response.out.write(template.render({
					'trackings' : models.Tracking.all()
				}))
		else:
			self.redirect(users.create_login_url(self.request.uri))
	
	def post(self):
		user = users.get_current_user()
		if not user:
			return
		newTracking = models.Tracking()
		newTracking.url = self.request.get("url")
		newTracking.put()
		return self.get()