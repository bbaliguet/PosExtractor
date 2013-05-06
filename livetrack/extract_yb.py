# Python 2.7
# -*- coding: UTF-8 -*-

import urllib, re, geo, math
from datetime import datetime
from xml.etree.cElementTree import ElementTree
from xml.etree.cElementTree import XMLParser

def extract_positions(url):
	tree = ElementTree()
	parser = XMLParser(encoding="iso-8859-1")
	data = urllib.urlopen(url)
	tree.parse(data, parser=parser)
	positions = tree.getroot().findall("team")
	allpos = []
	for pos in positions:
		realpos = pos.find("pos")
		latitude = float(realpos.attrib['a'])
		longitude = float(realpos.attrib['o'])
		speed = float(realpos.attrib['s'])
		course = float(realpos.attrib['c'])
		last_update = datetime.utcfromtimestamp(int(realpos.attrib["w"]))
		dtf = float(realpos.attrib['d'])

		_id = pos.attrib["id"]
		# pos = geo.xyz(latitude, latitude)

		# final object
		result = {}
		result["str_latitude"] = format_deg(latitude, "N", "S")
		result["str_longitude"] = format_deg(longitude, "E", "W")
		result["speed"] = speed
		result["course"] = course
		result["_id"] = _id
		result["dtf"] = dtf
		result["last_update"] = last_update

		allpos.append(result)
	return allpos

def extract_teams(url):
	tree = ElementTree()
	parser = XMLParser(encoding="iso-8859-1")
	data = urllib.urlopen(url)
	tree.parse(data, parser=parser)
	teams = tree.getroot().find("teams").findall("team")
	allteams = {}
	for team in teams:
		name = team.attrib["name"]
		_id = team.attrib["id"]
		sail = team.attrib["sail"]
		allteams[_id] = "{0} ({1})".format(name, sail)
	return allteams


def extract_yb(url):
	teams = extract_teams(url + "/TeamSetup")
	positions = extract_positions(url + "/LatestPositions")
	
	#merge everything
	for pos in positions:
		pos["name"] = teams[pos["_id"]]

	return positions


def format_deg(num, pos, neg):
	if num >= 0:
		adjust = pos
	else:
		adjust = neg
		num = -num
	deg = math.floor(num)
	minutes =math.floor((num - deg) * 60)
	sec = math.floor((num - deg - minutes / 60) * 3600)
	return "{0} {1}&deg;{2}'{3}''".format(adjust, int(deg), int(minutes), int(sec))
	