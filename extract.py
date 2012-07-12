import urllib,re

# Extract kml links from target url
# Python 2.7
def extractKml(url):
	data = urllib.urlopen(url)
	content = data.read()
	return extractLinks(content, url, ".kml")

def extractLinks(content, url, extension):
	links = set([])
	pattern = re.compile("href=['\"][^'\"]+" + extension + "['\"]", re.IGNORECASE)	
	matches = pattern.findall(content)
	queryString = url.find("?")
	base = url
	baseSlash = url
	if queryString != -1:
		base = url[0:queryString]
	lastSlash = url.rfind("/")
	if lastSlash != -1:
		baseSlash = url[0:lastSlash + 1]

	for match in matches:
		pathMatch=match[6:len(match)-1]
		if pathMatch[0:4] != 'http' and pathMatch[0:2] != "//" and pathMatch[0] != "#":
			if pathMatch[0] == "?":
				newUrl = base + pathMatch
			elif pathMatch[0] == "/":
				newUrl = url + pathMatch
			else:
				newUrl = baseSlash + pathMatch
			links.add(newUrl)
	return links