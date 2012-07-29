import re
from livetrack import extract
from google.appengine.ext import db

class Tracking(db.Model):
	active = db.BooleanProperty(default = False)
	url = db.StringProperty()

class MovingObject(db.Model):
	name = db.StringProperty()
	rating = db.FloatProperty()

class PosUpdate(db.Model):
	pos = db.GeoPtProperty()
	speed = db.FloatProperty()
	course = db.FloatProperty()
	date = db.DateProperty()


