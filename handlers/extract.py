# cron extractor
import webapp2
from livetrack import models, extract

class ExtractHandler(webapp2.RequestHandler):
	def get(self):
		trackings = models.Tracking.all()
		for tracking in trackings:
			if tracking.active:
				self.response.out.write(tracking.url + "<br/>")
				raws = extract.extract_pos(tracking.url)


