import re
from livetrack import extract
from google.appengine.ext import db

class Tracking(db.Model):
	active = db.BooleanProperty(default = False)
	url = db.StringProperty(required = True)
	dataType = db.StringProperty(required = True)
	kmls = db.StringListProperty()

class MovingObject(db.Model):
	name = db.StringProperty()
	rating = db.FloatProperty()

class PosUpdate(db.Model):
	name = db.StringProperty()
	pos = db.GeoPtProperty()
	speed = db.FloatProperty()
	course = db.FloatProperty()
	date = db.DateTimeProperty()
	latitude = db.StringProperty()
	longitude = db.StringProperty()


