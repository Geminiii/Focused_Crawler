import logging
import urllib
import urllib.parse
import urllib.request
from urllib.error import URLError
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
				file_size = int(response.info().get("content-length") or 0)/1000.0
				log_header += " Size: " + str(file_size) + " KB "
				print(response.read())
			self.logger.debug(log_header)
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
			self.total_failed += 1
			self.logger.error(url + " Unexpected error happened! ")




			#page = response.read()
			#print(page)
def main():
	downloader = Downloader()
	downloader.download('https://www.tutorialspoint.com/http/http_header_fields.htm')
	downloader.download('http://httpstat.us/200')
	"""downloader.download('http://httpstat.us/404')
	downloader.download('http://httpstat.us/503')
	downloader.download('http://httpstat.us/201')
	downloader.download('http://httpstat.us/401')
	downloader.download('http://httpstat.us/501')
	downloader.download('http://httpstat.us/202')
	downloader.download('http://httpstat.us/402')
	downloader.download('http://httpstat.us/502')
	downloader.download('http://httpstat.us/203')
	downloader.download('http://httpstat.us/403')
	downloader.download('http://httpstat.us/504')"""
if __name__ == '__main__':
	import logging.config
	logging.config.dictConfig(LOGGING)
	main()