# cron extractor
import webapp2, jinja2, os
from livetrack import models
from livetrack.extract import extract_pos
from google.appengine.ext import deferred

# jinja configuration
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def extract_and_store(link, key):
	result = extract_pos(link)
	if result:
		parent = models.Tracking.get(key)
		pos = models.PosUpdate()
		pos.course = result["course"]
		pos.speed = result["speed"]
		pos.date = result["last_update"]
		pos.latitude = result["str_latitude"]
		pos.longitude = result["str_longitude"]
		pos.name = result["name"]
		pos.parent = parent
		pos.put()

class ExtractHandler(webapp2.RequestHandler):
	def get(self):
		#clean previous
		previous = models.PosUpdate().all()
		for prev in previous:
			prev.delete()

		trackings = models.Tracking.all()
		for tracking in trackings:
			if tracking.active:
				kmls = tracking.kmls
				for link in kmls:
					self.response.out.write("<div>process {0}<div>".format(link))
					# deferred.defer(extract_and_store, link, tracking.key())
					extract_and_store(link, tracking.key())