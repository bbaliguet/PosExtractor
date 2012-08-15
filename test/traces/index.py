import os

files = open("index.html", "w")
files.write("<html><body>")

folder = os.listdir(".")
for f in folder:
	files.write("<div><a href='{0}'>{0}</a></div>".format(f))

files.write("</body></html>")
