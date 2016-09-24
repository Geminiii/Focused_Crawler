import logging
import os, sys
import urllib
import urllib.parse
import urllib.request
from urllib.error import URLError
from urllib.parse import urlparse
from loggingconfig import LOGGING

class Downloader(object):

	def __init__(self):
		self.logger=logging.getLogger(__name__)
		self.total_requests = 0
		self.total_404errors = 0
		self.total_failed = 0

	def download(self,url):
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
		values = {'name': 'Tianhao',
				'location': 'NYC',
				'language': 'Python'}
		headers = {'User-Agent': user_agent}
		data = urllib.parse.urlencode(values)
		data = data.encode('ascii')
		req = urllib.request.Request(url, data, headers)

		log_header = url + " Response Code: "

		try:
			response = urllib.request.urlopen(req)
			log_header += str(response.getcode())
			if response.getcode() == 200:
				content_type = response.info().get("content-type")
				content_length = response.info().get("content-length")
				if content_type.startswith("text/html"):
					if content_length:
						file_size = int( content_length or 0)/1000.0
					else:
						file_size = "Unknown"
					
					log_header += " Size: " + str(file_size) + " KB "
					text = response.read()
					self.logger.debug(log_header)
					try:
						self.writer(url, text)
					except :
						self.logger.error(log_header + "Cannot be written to disks!")
				else:
					log_header += " Unwanted file type, URL discarded "
					text = ""
				self.logger.debug(log_header)
				#self.writer(url, text)
				#return text
		except URLError as e:
			self.total_failed += 1
			if hasattr(e, 'reason'):
				if hasattr(e, 'code'):
					log_header += str(e.code) + " " + str(e.reason)
					if e.code == 404:
						self.total_404errors += 1
				else:
					log_header += str(e.reason)
				self.logger.error(log_header)
				
		except:
			print(urllib.request.urlopen(req).info())
			self.total_failed += 1
			self.logger.error(url + " Unexpected error happened! ")


	def writer(self, url, text):
		url_components = urlparse(url)
		#print(url_components)
		dir = './data/' + url_components.netloc + url_components.path
		#print(dir)
		if not os.path.isdir(dir):
			os.makedirs(dir)
		f = open(dir + '/index.html', 'w')
		f.write(str(text))
		f.close()

def main():
	downloader = Downloader()
	downloader.download('https://www.tutorialspoint.com/http/http_header_fields.htm')
	downloader.download('https://www.tutorialspoint.com/http/http_parameters.htm')

	downloader.download('http://cs.wellesley.edu/~qtw/lectures/webcrawl.html')
	downloader.download('http://stackoverflow.com/questions/27747288/python-name-os-is-not-defined-even-though-it-is-explicitly-imported')

	"""downloader.download('http://infolab.stanford.edu/pub/papers/google.pdf')
	downloader.download('http://httpstat.us/404')
	downloader.download('http://httpstat.us/503')
	downloader.download('http://httpstat.us/201')
	downloader.download('http://httpstat.us/403')
	downloader.download('http://httpstat.us/504')"""
if __name__ == '__main__':
	import logging.config
	logging.config.dictConfig(LOGGING)
	main()