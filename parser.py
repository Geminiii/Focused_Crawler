from linksExtractor import MyHTMLParser

class Parser(object):
	def __init__(self, query, url, content):
		self.query = query
		self.url = url
		self.content = content

	def extract_all_links(self):
		my_html_parser = MyHTMLParser()
		my_html_parser.feed(self.content)
		
		return my_html_parser.links