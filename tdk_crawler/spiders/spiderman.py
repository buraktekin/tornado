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
__email__ = "tekinbk@ims.uni-stuttgart.de"
__status__ = "Production"
__credits__ = [
	{
		'contributor': 'https://github.com/mertemin/turkish-word-list',
		'contribution': 'Turkish word list'
	}
]

# RECIPE: 
# ---------------------------------------------------------
# listofwords -> Spider -> Object (key, value pairs),
# Object: {word: "...", meaning: "..."}, type: JSON,
# word: String, meaning: String,
# ----------------------------------------------------------

import scrapy
import codecs
import json
import time
import os
import re

from definitions import ROOT_DIR
from scrapy.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tdk_crawler.items import TdkCrawlerItem

# ----------------------------------------------------------
# Problem
# ----------------------------------------------------------
# No implicit word list exist on web page and no links exist
# to follow to crawl recursively. Query string parameters
# are also hidden. 
#
# Solution:
# ----------------------------------------------------------
# The problem above lead me to use webdriver to make request
# with words and crawl the result pages have been responded.
# ----------------------------------------------------------


# Code:
# ----------------------------------------------------------
browser = webdriver.Chrome(ROOT_DIR + "/chromedriver")
browser.implicitly_wait(30)
browser.get("http://www.tdk.gov.tr/index.php?option=com_gts&arama=gts")

class Spiderman(CrawlSpider):
	name = 'tornado'

	def create_word_list(self):
		list_of_words = []
		with codecs.open(ROOT_DIR + '/words/words.txt', 'r', encoding='utf-8') as words:
			for word in words.readlines():
				list_of_words.append(word)

		return list_of_words

	def __init__(self):
		self.limit = 5
		self.allowed_domains = ["www.tdk.gov.tr"]
		self.start_urls = ["http://tdk.gov.tr/index.php?option=com_gts&arama=gts"]
		self.dictionary = self.create_word_list()


	def parse(self, response):
		word_no = 0
		data = dict()
		data['data'] = dict()

		while(word_no <= self.limit):
			word = self.dictionary[word_no].replace('\n','')
			time.sleep(1) # time's given to let the DOM updates itself
			input_field = browser.find_element_by_id('metin')
			browser.execute_script("arguments[0].value = ''", input_field) # Update input field to request words
			input_field.send_keys(word, Keys.RETURN)

			# get source of the page returned after request
			source = browser.page_source
			hxs = scrapy.Selector(text=source)
			meanings = hxs.xpath("//*[@id='hor-minimalist-a']/tbody/tr/td").extract()
			list_of_meanings = []
			list_of_meta_data = []
			for (index, meaning) in enumerate(meanings):
				meaning = meaning.replace('\n\t\t', '').strip()
				meaning_cleaned = re.findall(r'</i>(.*)<br>', meaning)
				meta_data = re.findall(r'<i>(.*)</i>', meaning)

				list_of_meanings.append(meaning)
				list_of_meta_data.append(meta_data)

				print "\n", list_of_meanings, list_of_meta_data
				
				item = TdkCrawlerItem()
				item['meaning'] = meaning_cleaned[0]
				item['meta_data'] = meta_data[0]
				item = dict(item)
				
				if(word in data):
					data['data'][word].append(item)
				else:
					data['data'][word] = [item]

			# Next word...
			word_no += 1
		yield data




