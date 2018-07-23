__author__ = 'RAYMOND'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

#qiushibaike class
class QSBK(object):
	"""docstring for QSBK"""
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#init headers
		self.headers = {'User-Agent' : self.user_agent}
		#var for saving duanzi 
		self.stories = []
		#continue or not
		self.enable = True

	#get Page source code
	def getPage(self, pageIndex):

		try:
			url = 'http://www.qiushibaike.com/hot/page' + str(pageIndex)
			#create  a request
			request = urllib2.Request(url, headers=self.headers)
			#get response
			respone = urllib2.urlopen(request)
			#get pageCode
			pageCode = respone.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, reason):
				print u'fail to connect, reason: ', e.reason
				return None
	#get page items
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print u'fail to load ....'
			return None
		pattern = re.compile('<h2>(.*?)</h2>.*?<div.*?content.*?<span>(.*?)</span>.*?<!--(.*?)<div.*?stats.*?number">(.*?)</i>',re.S)
		items = re.findall(pattern, pageCode)
		pageStories = []
		for item in items:
			#have img or not 
			haveImg = re.search('img', item[2])
			if not haveImg:
				#get text
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR,"\n", item[1])
				#save duanzi to a story list of one page
				pageStories.append([item[0].strip(), text.strip(), item[1].strip()])
		return pageStories
	#load and read pages, add to top list
	def loadPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				#load a new page 
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	#get one story for one time
	def getOneStory(self, pageStories, page):
		#look through one page's duanzi
		for story in pageStories:
			#waiting for user's input
			input = raw_input()
			self.loadPage()
			if input == 'Q':
				self.enable = False
				return
			print u'page:%d\tauthor:%s\tvotes:%s\n%s' %(page, story[0], story[2], story[1])
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







