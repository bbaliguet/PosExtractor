import webapp2, jinja2, os, logging
from google.appengine.api import users
from livetrack import models, extract

# jinja configuration
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def check_user(handler):
	user = users.get_current_user()
	if user:
		return True
	else:	
		handler.response.status = 403
		return False

class ConfHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		uri = self.request.uri
		if user:
			template = jinja_environment.get_template('templates/conf.html')
			self.response.out.write(template.render({
					'logout_url' : users.create_logout_url(uri), 
					'trackings' : models.Tracking.all()
				}))
		else:	
			self.redirect(users.create_login_url(uri))
			
	
	def post(self):
		if check_user(self):
			newTracking = models.Tracking(url = self.request.get("url"))
			newTracking.put()
			self.response.out.write(newTracking.key())

	def delete(self):
		if check_user(self):
			key = self.request.get("id")
			tracking = models.Tracking.get(key)
			if tracking != None:
				tracking.delete()
			else:
				self.response.status = 400

	def put(self):
		if check_user(self):
			key = self.request.get("id")
			tracking = models.Tracking.get(key)
			if tracking != None:
				tracking.active = not tracking.active
				self.response.out.write("1" if tracking.active else "0")
				if tracking.active:
					links = extract.extract_kml(tracking.url)
					tracking.kmls = links
				tracking.put()
			else:
				self.response.status = 400

