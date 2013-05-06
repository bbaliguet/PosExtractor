import urllib
from livetrack.extract import extract_kml, extract_pos
from livetrack.extract_yb import extract_yb
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

def test_extract_local():
	links = extract_kml("http://www.sat-view.fr/comptes/celtikup/traces/")
	for link in links:
		raw = extract_pos(link)
		print raw

def test_extract_yb():
	teams = extract_yb("http://yb.tl/Flash/t2p2013")
	for team in teams:
		print team

if __name__ == '__main__':
	test_extract_yb()