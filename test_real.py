import urllib
from livetrack.extract import extract_kml, extract_pos
from livetrack.extract_yb import extract_yb
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLParser


def test_extract():
	# links = extract_kml("http://www.sat-view.fr/comptes/celtikup/traces/")
	links = extract_kml("http://www.sat-view.fr/comptes/snst/traces/")
	for link_struct in links:
		link = link_struct.link
		data = urllib.urlopen(link)
		target = "test/traces/" + link[43:len(link)]
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
	test_extract()