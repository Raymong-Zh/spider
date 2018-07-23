__author__ = 'Raymond'
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

#qiushibaike class
class QSBK(object):
	"""docstring for QSBK"""
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#init headers
		self.headers = {'User-Agent' : self.user_agent}
		#var for saving duanzi, one element for one page's duanzi
		self.stories = []
		#var for continuing  to run or not
		self.enable = False
	#get one page
	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page' + str(pageIndex)
			#create request
			request = urllib2.Request(url, headers=self.headers)
			#get response
			response = urllib2.urlopen(request)
			#get pageCode
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u'fail to connect qiushibaike, reason: ', e.reason
				return None
	#get items in one page
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "fail to load page ..."
			return None
		pattern = re.compile('<h2>(.*?)</h2>.*?<div.*?content.*?<span>(.*?)</span>.*?<!--(.*?)<div.*?stats.*?number">(.*?)</i>',re.S)
		items = re.findall(pattern, pageCode)
		#var for saving duanzi in one page
		pageStories = []
		#look through items
		for item in items:
			#have img or not
			haveImg = re.search('img', item[2])
			if not haveImg:
				replaceBR =re.compile('<br/>')
				text = re.sub(replaceBR, "\n", item[1])
				#item[0] for author; item[1] for duanzi; item[3] for votes
				pageStories.append([item[0].strip(), text.strip(),item[3].strip()])
		return pageStories
		#pageStories is a list of lists
	#load and read the page, add to list 
	def loadPage(self):
		#if page num less than 2, load a new one
		if self.enable == True:
			if len(self.stories) < 2:
				#load a new one
				pageStories = self.getPageItems(self.pageIndex)
				#save to the NO.1 list
				if pageStories:
					self.stories.append(pageStories)
					#next page
					self.pageIndex += 1
	def getOneStory(self, pageStories, page):
		#look through stories in one page
		for story in pageStories:
			#waiting for user's input
			input = raw_input()
			#Enter once  load a new page or not
			self.loadPage()
			# Q for quit
			if input == 'Q':
				self.enable = False
				return
			print u'page: %d\tauthor:%s\tvotes:%s\t\n%s' %(page, story[0],story[2],story[1])
	#start function
	def start(self):
		print u'loading qiushibaike, Enter for new one, Q for quit'
		#enable 
		self.enable = True
		#load one page
		self.loadPage()
		#nowPage
		nowPage = 0
		while self.enable:
			if len(self.stories) >0:
				#get one page's duanzi
				pageStories = self.stories[0]
				#nowPage +
				nowPage += 1
				#del the first page
				del self.stories[0]
				#output duanzi in this page
				self.getOneStory(pageStories,nowPage)
spider = QSBK()
spider.start()

		
		
		