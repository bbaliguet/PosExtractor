import urllib, re
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLParser

# Extract kml links from target url
# Python 2.7
def extractKml(url):
	data = urllib.urlopen(url)
	content = data.read()
	return extractLinks(content, url, ".kml")

def extractLinks(content, url, extension = ""):
	links = set([])
	pattern = re.compile("href=['\"][^'\"]+" + extension + "['\"]", re.IGNORECASE)	
	matches = pattern.findall(content)

	anchorPos = url.find("#")
	if anchorPos != -1:
		url = url[0:anchorPos]

	base = url

	queryString = base.find("?")
	if queryString != -1:
		base = base[0:queryString]

	baseSlash = base
	lastSlash = baseSlash.rfind("/")
	if lastSlash != -1:
		baseSlash = baseSlash[0:lastSlash + 1]

	for match in matches:
		pathMatch=match[6:len(match)-1]
		if pathMatch[0:4] == 'http' or pathMatch[0:2] == "//":
			links.add(pathMatch)
		elif pathMatch[0] == "#":
			links.add(url+pathMatch)
		elif pathMatch[0] == "?":
			links.add(base+pathMatch)
		else:
			links.add(baseSlash+pathMatch)
	return links

def extractPos(url):
	links = extractKml(url)
	for link in links:
		print link
		data = urllib.urlopen(link)
		tree = ElementTree()
		parser = XMLParser(encoding="iso-8859-1")
		tree.parse(data, parser=parser)
		posName = tree.findtext('kml')
		print posName
