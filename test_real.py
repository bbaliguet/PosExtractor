from livetrack.extract import extract_pos
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLParser


def extract():
	extract_pos("http://www.sat-view.fr/comptes/celtikup/traces/")

if __name__ == '__main__':
	extract()