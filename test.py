# -*- coding: UTF-8 -*-

import unittest, sys
from livetrack import extract

class TestExtract(unittest.TestCase):
	def test_extract_links(self):
		test = open("test/testExtractLinks.html")
		test_content = test.read()
		test.close()
		links = extract.extract_links(test_content, "http://test/test", ".ext")
		self.assertIn("http://test/test1.ext", links)
		self.assertIn("http://test//test4.ext", links)

		links = extract.extract_links(test_content, "http://test/test")
		self.assertIn("http://test/test3.ext#anchor", links)
		self.assertIn("http://google.com", links)
		self.assertIn("http://test//test4.ext", links)
		self.assertIn("http://test/test1.ext", links)
		self.assertIn("http://test/test2.other", links)
		self.assertIn("http://test/test/test5.ext?something=somethingElse", links)

	def test_updateModel(self):
		raw="""<hr>
<b>Skipper: </b>René BERSON<br>
<b>Equipier: </b>Franck BERSON<br>
<b>Bateau: </b>BAVARIA 35 MATCH<br>
<b>Classe: </b>HN<br>
<hr>
<b>Date et heure du dernier point : </b><br>
13/08/2011 21:40:21 (heure d'été)<br>
<b>Dernière mise à jour de la carte: </b><br>
15/08/2011 01:59:55<br>
<hr>
<b>Latitude: </b> N 47 43'30''<br>
<b>Longitude: </b> W 003 20'59''<br>
<b>Cap: </b> 111 °<br>
<b>Vitesse: </b> 0.38 kts<br>
<b>Distance parcourue: </b> 439.72 Nm<br>
<hr>"""
		lat = extract.prop_raw_extract("Latitude", raw)
		self.assertEqual(lat, "N 47 43'30''")
		last_update = extract.prop_raw_extract("Date et heure du dernier point ", raw, True)
		self.assertEqual(last_update, "13/08/2011 21:40:21 (heure d'été)")

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestExtract)
	result = unittest.TextTestRunner().run(suite)
	if not result.wasSuccessful():
		sys.exit(1)

