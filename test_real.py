import urllib
from livetrack.extract import extract_kml
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLParser


def extract():
	links = extract_kml("http://www.sat-view.fr/comptes/celtikup/traces/")
	for link in links:
		data = urllib.urlopen(link)
		target = "test/traces/" + link[47:len(link)]
		print target
		f = open(target, "w")
		f.write(data.read())

if __name__ == '__main__':
	extract()