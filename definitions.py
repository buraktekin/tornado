# -*- coding: utf-8 -*-
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def parse(self, response):
	word_no = 0

	while(word_no <= self.limit):
		word = self.dictionary[word_no]

		# Update input field to request words
		input_field = browser.find_element_by_id('metin')
		browser.execute_script("arguments[0].value = ''", input_field)
		input_field.send_keys(word)
		input_field.send_keys(Keys.RETURN)
		# time's given to let the DOM updates itself
		time.sleep(0.2)

    # get source of the page returned after request
		source = browser.page_source
		hxs = scrapy.Selector(text=source)
		meanings = hxs.xpath("//table[@id='hor-minimalist-a']/tbody/tr/text()").extract()
		for meaning in meanings:
			yield scrapy.http.Request(
				meta={'meta_data': meta_data, 'word': word, 'meaning': meaning}, 
				callback=self.create_item
			)

		# Next word...
		word_no += 1

def create_item(self, response):
	meta_data = response.meta['meaning'].xpath(".//td/i/text()").extract_first()
	# Add words and meanings
	item = NcbiCrawlerItem()
	item["meta_data"] = meta_data
	item["word"] = word
	item["meaning"] = meaning