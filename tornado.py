# -*- coding: utf-8 -*-


# Project: TORNADO
# ---------------------------------------------------------
# Purpose: Crawling Turkish Language Society's web page
# (tdk.gov.tr) to get Turkish words and their meanings to 
# provide a better service to people who want to contribute
# improvement of Turkish language studies.
# ---------------------------------------------------------
__author__ = "Datallite"
__copyright__ = "Copyleft 2019, Project Tornado"
__license__ = "MIT"
__version__ = "0.0.1"
__email__ = "datallite@web.de"
__status__ = "Staging"
__credits__ = [
	{
		'contributor': 'https://github.com/mertemin',
		'contribution': 'Turkish word list'
	}
]

import os
import typing
import requests
import contextlib

project_dir = os.path.dirname(os.path.abspath(__file__))

class Tornado:
    def __init__(self, source_url, list_of_paths):
        self.source_url = source_url
        self.list_of_paths = list_of_paths
    
    def read_word_list(self):
        with contextlib.ExitStack() as stack:
            files = [stack.enter_context(open(path)) for path in self.list_of_paths]

        for file in files:
            print(file)

if __name__ == '__main__':
    instance = Tornado("http://sozluk.gov.tr/gts?ara=", [project_dir + "/words/word_sample.txt"])
    instance.read_word_list()
