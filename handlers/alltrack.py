# cron extractor
import webapp2, jinja2, os, geo
from livetrack import models
from livetrack.extract import extract_pos
from google.appengine.ext import deferred

# jinja configuration
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class AllHandler(webapp2.RequestHandler):
	def get(self):
		trackings = models.Tracking.all()
		results = []
		for tracking in trackings:
			if tracking.active:
				kmls = tracking.kmls
				for link in kmls:
					res = extract_pos(link)
					if res:
						results.append(res)
		template = jinja_environment.get_template('templates/all.html')
		
		#prepare for svg
		latmin = results[0]["latitude"]
		latmax = results[0]["latitude"]
		longmin = results[0]["longitude"]
		longmax = results[0]["longitude"]
		for result in results:
			latmin = min(latmin, result["latitude"])
			latmax = max(latmax, result["latitude"])
			longmin = min(longmin, result["longitude"])
			longmax = max(longmax, result["longitude"])

		latmin = latmin - (latmax - latmin) / 10
		latmax = latmax + (latmax - latmin) / 10
		deltalat = latmax - latmin
		longmin = longmin - (longmax - longmin) / 10
		longmax = longmax + (longmax - longmin) / 10
		deltalong = longmax - longmin
		latmiddle = (latmax + latmin) / 2
		longmiddle = (longmax + longmin) / 2

		verticalAdjust = geo.distance(geo.xyz(latmiddle, longmin), 
			geo.xyz(latmiddle, longmax)) / geo.distance(geo.xyz(latmin, longmiddle), 
			geo.xyz(latmax, longmiddle)) * 800

		for result in results:
			result["posX"] = (latmax - result["latitude"]) / deltalat * 800
			result["posY"] = (result["longitude"] - longmin) / deltalong * verticalAdjust

		self.response.out.write(template.render({
			'extracts' : sorted(results, key=lambda extract: extract["dtf"]),
			'verticalAdjust' : verticalAdjust
		}))
