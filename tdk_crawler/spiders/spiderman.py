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

# RECIPE: 
# ---------------------------------------------------------
# listofwords(list) -> Spider() -> Output(JSON format file)
# Output Object: {word: {meaning: ["..."], meta: [...]}
# word: String, meaning: listofstring, meta_data: listofString
# ----------------------------------------------------------

# ----------------------------------------------------------
# Problem
# ----------------------------------------------------------
# No implicit word list exist on web page and no links exist
# to follow to crawl the page recursively. Query string 
# parameters are also hidden.
#
# Solution:
# ----------------------------------------------------------
# The problem above lead me to use webdriver to make request
# with words and crawl the result pages have been responded.
# ----------------------------------------------------------


# Code:
# ----------------------------------------------------------
import scrapy
import codecs
import json
import time
import sys
import os
import re

from definitions import ROOT_DIR
from scrapy.spiders import CrawlSpider
from tdk_crawler.modules.parser import Parser

class Spiderman(CrawlSpider):
	name = 'tornado'
	data = dict()


	def create_word_list(self):
		list_of_words = []
		with codecs.open(ROOT_DIR + '/words/words.txt', 'r', encoding='utf-8') as words:
			for word in words.readlines():
				list_of_words.append(word.encode('utf-8').replace('\n', ''))

		return list_of_words


	def __init__(self):
		self.url = 'http://www.tdk.gov.tr/index.php?option=com_gts&kelime='
		self.dictionary = self.create_word_list()
		self.allowed_domains = ["www.tdk.gov.tr"]
		self.start_urls = [self.url]
		self.parser = Parser()


	def word_log(self, word):
		now = time.strftime("%c")
		line = ""
		with codecs.open(ROOT_DIR + '/words_missing.log', 'a+', encoding='utf-8') as log:
			log.seek(0)
			first_char = log.read()
			if(first_char):
				line = "<word>"+word + "</word>" + "\t" + now + "\n"
			else:
				line = "Missing word\tlog_saved_at\n"
			
			log.write(line)
			log.flush()


	def parse(self, response):
		try:
			for (index, word) in enumerate(self.dictionary):
				url = self.url + word
				yield scrapy.http.Request(
					url=url, 
					meta={'word': word, 'word_no': index}, 
					callback=self.parse_recursively
				)
		except:
			print("Oops!",sys.exc_info()[0],"occured.")
			self.word_log(word)
			print("Next word...")


	def parse_recursively(self, response):
		word = response.meta['word'].decode('utf-8')
		word_no = response.meta['word_no']
		hxs = scrapy.Selector(response)
		meanings = hxs.xpath("//table[@id='hor-minimalist-a']").extract()
		print "\nCurrent Word: \t" + word + "\n" + "Word No: " + str(word_no) + "\n"

		for meaning in meanings:
			parsed_text = self.parser.get_texts_from_tags(meaning)
			if(word in self.data):
				self.data[word].append(parsed_text)
			else:
				self.data[word] = [parsed_text]

		return self.data



