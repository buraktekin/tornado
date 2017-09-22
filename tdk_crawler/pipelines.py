# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class TdkCrawlerPipeline(object):

	def __init__(self):
		self.file = codecs.open('data_encoded.json', 'w', encoding='utf-8')

	# def process_item(self, item, spider):
		# return item

	def close_spider(self, spider):
		line = json.dumps(dict(spider.data), 
			sort_keys=True, 
			indent=4,
			ensure_ascii=False, 
		)
		self.file.write(line)
		self.file.close()