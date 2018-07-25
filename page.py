# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import time
import types
import zhishitool
from bs4 import BeautifulSoup

#get the question and answers
class Page(object):
	"""docstring for Page"""
	def __init__(self):
		self.tool = zhishitool.Tool()
		
