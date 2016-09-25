import pprint
import logging
import urltools
import urllib
from urllib import robotparser
from urllib.parse import urlparse
from loggingconfig import LOGGING
from googleapiclient.discovery import build
from pqdict import PQDict
from downloader import Downloader


#parameters for google search API:
API_KEY="AIzaSyBsx7wuJfoHIA9VsWayDFZW-w7APu-4gps"
SEARCH_ENGINE_ID = '012502276015408778302:aanpptkeffi'


class Crawler():

	def __init__(self):

		self.query = input("Enter search query: ")
		self.webpages_limit = input("Set total number of webpages to be crawled: ")
		self.limit = input("Set limits on how many webpages be crawled from single site: ")
		self.priority_queue = PQDict().maxpq()
		self.downloader = Downloader()
		self.webpages_crawled = 0
		self.logger = logging.getLogger(__name__)
		self.visited_urls = {}
		self.sites_times = {}
	#fetch top 10 results from google search:
	def __fetch_google_results(self):
		service = build("customsearch","v1",developerKey=API_KEY)
		res =service.cse().list(
			q= self.query,
			cx= SEARCH_ENGINE_ID).execute()
		return res
	#enqueue the 10 google search results 
	def enqueue_seeds(self):
		res=self.__fetch_google_results()
		for item in res['items']:
			self.priority_queue.additem(item['link'],10)
			self.logger.debug("Enqueued: "+ item['link'])
			self.webpages_crawled+=1
	#check has this url been visited before
	#and has it reach the limit of each site
	#and Robot Exclusion Protocols
	def urlchecker (self, url):

		normalized_url = urltools.normalize(url)
		robotparser = urllib.robotparser.RobotFileParser()
		try:
			url_comp = urlparse(normalized_url)
			base_url = url_comp.scheme + "://" + url_comp.netloc + "/"
		except:
			self.logger.error("Cannot parse: " + url)
		try:
			robotparser.set_url(base_url + "robots.txt")
			robotparser.read()
			if not robotparser.can_fetch("*", normalized_url):
				self.logger.error(url + " is excluded due to protocol")
				return False
		except:
			self.logger.error("Cannot determine robots exclusion protocol: " + url)

		if normalized_url in self.visited_urls:
			self.logger.debug(url + " Has been visited before! ")
			return False
		elif base_url in self.sites_times and self.sites_times[base_url] > self.limit :
			#self.visited_urls[url] = True
			self.logger.debug(url + " Times visiting this site have reach the limit ")
			return False
		else:
			return True
	#the crawling process
	def crawl(self):
		try:
			while self.priority_queue.top():
				url = self.priority_queue.pop()
				if self.urlchecker(url):
					try:
						text = self.downloader.download(url)
					except :
						print( "Failed in downloading")



				else:
					self.logger.debug(url + " CANNOT been crawled due to previous reason")
		except KeyError :
			print ("Queue is empty now")
			#self.logger.error(" Key does not exist or queue is empty! ")


def main():
	crawler = Crawler()
	crawler.enqueue_seeds()

	crawler.crawl()
	



if __name__ == '__main__':
	import logging.config
	logging.config.dictConfig(LOGGING)
	#logging.config.fileConfig('logging1.config',disable_existing_loggers=False)
	main()