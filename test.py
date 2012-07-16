import livetrack.extract, unittest

class TestExtract(unittest.TestCase):
	def test_extractLinks(self):
		test = open("test/testExtractLinks.html")
		testContent = test.read()
		test.close()
		links = livetrack.extract.extractLinks(testContent, "http://test/test", ".ext")
		self.assertIn("http://test/test1.ext", links)
		self.assertIn("http://test//test4.ext", links)

		links = livetrack.extract.extractLinks(testContent, "http://test/test")
		self.assertIn("http://test/test3.ext#anchor", links)
		self.assertIn("http://google.com", links)
		self.assertIn("http://test//test4.ext", links)
		self.assertIn("http://test/test1.ext", links)
		self.assertIn("http://test/test2.other", links)
		self.assertIn("http://test/test/test5.ext?something=somethingElse", links)
		
if __name__ == '__main__':
	unittest.main()

