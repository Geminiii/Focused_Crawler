from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
	def __init__(self):

	def handle_starttag(self, tag, attrs):
		if tag.lower() == 'a':
			for attr, value in attrs:
				if key == 'href':
					


	def handle_endtag(self, tag):


	def handle_data(self, data):
