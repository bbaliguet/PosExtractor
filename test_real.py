from livetrack.extract import extractPos
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLParser


def extract():
	extractPos("http://www.sat-view.fr/comptes/celtikup/traces/")

if __name__ == '__main__':
	extract()