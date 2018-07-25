# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import time
import types
import page
import mysql
import sys
from bs4 import BeautifulSoup

class Zhishi(object):
	"""docstring for Zhishi"""
	def __init__(self):
		self.page_num = 1
		self.total_num = None
		self.page_spider = page.Page()
		self.mysql = mysql.Mysql()

	#get current time
	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

	#get current date
	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d', time.localtime(time.time()))


		
