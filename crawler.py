import pprint
import logging
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
		self.webpages_limit=input("Set total number of webpages to be crawled: ")
		self.priory_queue= PQDict().maxpq()
		self.webpages_crawled=0
		self.logger=logging.getLogger(__name__)
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
			self.priory_queue.additem(item['link'],10)
			self.logger.debug("Enqueued: "+ item['link'])
			self.webpages_crawled+=1
	
	def crawl(self):
		try:
			url = priory_queue.pop()

		except KeyError :
			self.logger.error(" Key does not exist or queue is empty! ")


def main():
	crawler = Crawler()
	crawler.enqueue_seeds()
	#for item in crawler.priory_queue:
	pprint.pprint(crawler.priory_queue)



if __name__ == '__main__':
	import logging.config
	logging.config.dictConfig(LOGGING)
	#logging.config.fileConfig('logging1.config',disable_existing_loggers=False)
	main()