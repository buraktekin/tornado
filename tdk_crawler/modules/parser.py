# -*- coding: utf-8 -*-

# Project: TORNADO
# ---------------------------------------------------------
# Purpose: Crawling Turkish Language Society's web page
# (tdk.gov.tr) to get Turkish words and their meanings to 
# provide a better service to people who want to contribute
# improvement of Turkish language studies.
# ---------------------------------------------------------
__author__ = "Burak Tekin"
__copyright__ = "Copyleft 2017, Project Tornado"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "tknbrk@gmail.com"
__status__ = "Staging"
__credits__ = [
	{
		'contributor': 'https://github.com/mertemin',
		'contribution': 'Turkish word list'
	}
]

# Module: TEXT PARSER
# ---------------------------------------------------------
# Purpose: Split crawled text into two parts which are:
# 	meaning: The meaning of the corresponding word.
# 	meta: The POS tag and the root of the word coming from
# ---------------------------------------------------------

# Important Notes:
# ---------------------------------------------------------
# The way of serving pages in this website is definitely a
# disaster. There is no any well structured semantic component
# through the pages. Hence, this part is essential to set 
# a structure for words and its information. You can easily
# see that there are several regex used in the method below
# to clean the data fetched from all incoherent characters it
# has and split it into different(3) fields.
# ---------------------------------------------------------
import re

from BeautifulSoup import BeautifulSoup
from tdk_crawler.items import TdkCrawlerItem

class Parser():
	def __init__(self):
		self.meta = ""
		self.meaning = ""
		self.example = ""
		


	def parse_header(self, source, soup):
		header_container = list()
		for header in soup.findAll('th'):
			header_info = header.find('i')
			header_meta = header_info.find('b').getText().strip()
			header_info = header_info.text.replace(header_meta, '', 1).strip()
			header_container.append(header_meta + " " + header_info)
		return header_container

	def parse_body(self, source, soup):
		body_container = list()
		source = re.sub(r'<b>(.*)</b>', '', source)
		source = source.replace('\n\t\t', '')
		for node in soup.findAll('td'):
			text = re.findall('\"(.*)', node.getText())
			self.example = text[0] if len(text) > 0 else ""
			self.meta = node.find('i').getText()
			self.meaning = node.text\
										.replace(self.meta,'', 1)\
										.replace(self.example, "")

			tdk_item = TdkCrawlerItem()
			tdk_item['meta'] = self.meta
			tdk_item['meaning'] = self.meaning.replace('\"', '')
			tdk_item['example'] = self.example.replace('\"', '')
			tdk_item = dict(tdk_item)
			body_container.append(tdk_item)	
		return body_container

	def get_texts_from_tags(self, source):
		container = dict()
		soup = BeautifulSoup(source)
		header_container = self.parse_header(source, soup)
		body_container = self.parse_body(source, soup)
		container['header'] = header_container
		container['body'] = body_container
		return container




