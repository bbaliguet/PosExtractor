import re
from google.appengine.ext import db

class point(db.Model):
	index = db.IntegerProperty()
	latitude = db.FloatProperty()
	longitude = db.FloatProperty()

class object(db.Model):
	name = db.StringProperty()
	rating = db.FloatProperty()

class update(db.Model):
	pos = db.GeoPtProperty()
	speed = db.FloatProperty()
	course = db.FloatProperty()
	date = db.DateProperty()