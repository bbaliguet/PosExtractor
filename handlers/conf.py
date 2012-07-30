import webapp2, jinja2, os
from google.appengine.api import users
from livetrack import models

# jinja configuration
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def check_user(handler):
	user = users.get_current_user()
	if user:
		return True
	else:	
		self.redirect(users.create_login_url(self.request.uri))
		return False

class ConfHandler(webapp2.RequestHandler):
	def get(self):
		if check_user(self):
			template = jinja_environment.get_template('templates/conf.html')
			self.response.out.write(template.render({
					'trackings' : models.Tracking.all()
				}))
	
	def post(self):
		if check_user(self):
			newTracking = models.Tracking(url = self.request.get("url"))
			newTracking.put()

	def delete(self):
		if check_user(self):
			id = self.request.get("id")
			tracking = models.Tracking.get_by_id(id)
			if tracking != None:
				tracking.delete()
			else:
				self.response.status = 400

