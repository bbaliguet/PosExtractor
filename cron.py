from livetrack import extract
from pymongo import MongoClient

# target = "http://www.sat-view.fr/comptes/celtikup/traces/"
target = "http://www.sat-view.fr/comptes/snst/traces/"

client = MongoClient()
db = client.tracking
tracks = db.tracks

if __name__ == '__main__':
	links = extract.extract_kml(target)
	for link_struct in links:
		link = link_struct.link
		tracks.insert({
			"result": extract.extract_pos(link),
			"date": link_struct.date
			})
