# Python 2.7

import urllib, re
from xml.etree.cElementTree import ElementTree
from xml.etree.cElementTree import XMLParser

# Extract kml links from target url
def extract_kml(url):
	data = urllib.urlopen(url)
	content = data.read()
	return extract_links(content, url, ".kml")

def extract_links(content, url, extension = ""):
	links = set([])
	pattern = re.compile("href=['\"][^'\"]+" + extension + "['\"]", re.IGNORECASE)	
	matches = pattern.findall(content)

	anchor_pos = url.find("#")
	if anchor_pos != -1:
		url = url[0:anchor_pos]

	base = url

	query_string = base.find("?")
	if query_string != -1:
		base = base[0:query_string]

	base_slash = base
	last_slash = base_slash.rfind("/")
	if last_slash != -1:
		base_slash = base_slash[0:last_slash + 1]

	for match in matches:
		path_match=match[6:len(match)-1]
		if path_match[0:4] == 'http' or path_match[0:2] == "//":
			links.add(path_match)
		elif path_match[0] == "#":
			links.add(url+path_match)
		elif path_match[0] == "?":
			links.add(base+path_match)
		else:
			links.add(base_slash+path_match)
	return links

def extract_pos(url):
	links = extract_kml(url)
	root_namespace_reg = re.compile("\{.*\}", re.IGNORECASE)
	root_namespace = None
	results = {}
	for link in links:
		try:
			data = urllib.urlopen(link)
			tree = ElementTree()
			parser = XMLParser(encoding="iso-8859-1")
			tree.parse(data, parser=parser)
			# do this only once, assume all files have the same
			if (root_namespace == None):
				root_namespace = root_namespace_reg.findall(tree.getroot().tag)[0]

			name = tree.find(".//{0}Document//{0}name".format(root_namespace)).text
			unparsed = tree.find(".//{0}Document//{0}Placemark//{0}description".format(root_namespace)).text
			result[name] = unparsed
		except:
			pass
	return results

def prop_raw_extract(prop, raw):
	search = re.search("(?<=<b>" + prop + "\: <\/b>).*(?=<br>)", raw)
	return search.group(0).strip()