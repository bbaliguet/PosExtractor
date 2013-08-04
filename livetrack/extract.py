# Python 2.7
# -*- coding: UTF-8 -*-

import urllib, re, geo
from datetime import datetime
from xml.etree.cElementTree import ElementTree
from xml.etree.cElementTree import XMLParser
from bs4 import BeautifulSoup

months = {"Jul" : "07", "Aug" : "08"}

class ExtractedLink:
	def __init__(self, link, date):
		self.link = link
		self.date = date

# Extract kml links from target url
def extract_kml(url):
	data = urllib.urlopen(url)
	content = data.read()
	links = extract_links(content, url, "c\\d{2}\\.kml")
	return links

def extract_links(content, url, extension = ""):
	parsed_html = BeautifulSoup(content)
	all_links = parsed_html.find_all("a")

	links = set([])
	pattern = re.compile(".*" + extension, re.IGNORECASE)
	for link in all_links:
		href = link["href"]
		match = re.search(pattern, href)
		if match:
			date = link.parent.next_sibling.string
			links.add(ExtractedLink(url+match.group(0), date))

	return list(links)

def extract_pos(link):
	root_namespace_reg = re.compile("\{.*\}", re.IGNORECASE)
	root_namespace = None
	try: 
		data = urllib.urlopen(link)
		tree = ElementTree()
		parser = XMLParser(encoding="iso-8859-1")
		tree.parse(data, parser=parser)
		root_namespace = root_namespace_reg.findall(tree.getroot().tag)[0]
		name = tree.find(".//{0}Document//{0}name".format(root_namespace)).text

		# parse important datas
		unparsed = tree.find(".//{0}Document//{0}Placemark//{0}description".format(root_namespace)).text
	except Exception, e:
		return

	result = parse_raw(unparsed)
	result["name"] = name

	return result

def prop_raw_extract(prop, raw, multiline = False):
	multiline_part = "<br>\\n" if multiline else "" 
	reg = re.compile("(?<=<b>" + prop + "\: <\/b>" + multiline_part + ").+(?=<br>)")
	search = re.search(reg, raw)
	if search:
		return search.group(0).strip()
	return None

def parse_raw(raw):
	result = {}
	num_regexp = re.compile("\d+(\.\d+)?")
	
	last_update = prop_raw_extract("Date et heure du dernier point ", raw, True)
	# remove "(heure d'été)"
	last_update = last_update[0:last_update.rfind("(")].strip()
	result["last_update"] = datetime.strptime(last_update, "%d/%m/%Y %H:%M:%S") 
	
	course = prop_raw_extract("Cap", raw)
	result["course"] = float(re.search(num_regexp, course).group(0))
	
	speed = prop_raw_extract("Vitesse", raw)
	result["speed"] = float(re.search(num_regexp, speed).group(0))

	latitude = prop_raw_extract("Latitude", raw)
	result["str_latitude"] = latitude
	south = latitude[0] == "S"
	split = re.findall("\d+", latitude)
	# N 47 43'30''
	numlatitude = float(split[0]) + float(split[1])/60 + float(split[2])/3600
	if south:
		numlatitude = -numlatitude
	result["latitude"] = numlatitude

	longitude = prop_raw_extract("Longitude", raw)
	result["str_longitude"] = longitude
	est = longitude[0] == "E"
	split = re.findall("\d+", longitude)
	# W 003 20'59''
	numlongitude = float(split[0]) + float(split[1])/60 + float(split[2])/3600
	if est:
		numlongitude = -numlongitude
	result["longitude"] = numlongitude

	pos = geo.xyz(numlatitude, numlongitude)
	# N 47 42,8 W 3 21,5 
	finish = geo.xyz(47.7133,3.3583)
	result["dtf"] = '%0.1f' % (geo.distance(pos, finish) / 1852)

	return result