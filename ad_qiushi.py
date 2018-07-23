__author__ ='Raymond'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

#define qiushibaike spider class
class QSBK(object):
	"""docstring for QSBK"""
	#initial some vars
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5 Windows NT)'
		#init headers
		self.headers = {'User-Agent' : self.user_agent}
		#save duanzi, one elment for one page's duanzi
		self.stories = []
		#if continue to save
		self.enable = False
	#input the page index, get source code of this page
	def getPage(self, pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			#create request
			request = urllib2.Request(url, headers = self.headers)
			#get source code by urlopen
			response = urllib2.urlopen(request)
			#decode to utf-8
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"connect qiushibaike fail, reason:", e.reason
				return None
	#input index of page, return duanzi list without imgs
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "load page fail..."
			return None
		pattern = re.compile('<h2>(.*?)</h2>.*?<div.*?content.*?<span>(.*?)</span>.*?<!--(.*?)<div.*?stats.*?number">(.*?)</i>',re.S)
		items = re.findall(pattern, pageCode)
		#save duanz in every page
		pageStories = []
		#lookthrough the pageCode
		for item in items:
			#has img or not
			haveImg = re.search("img", item[2])
			if not haveImg:
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR, "\n", item[1])
				#item[0] for author ;   item[1] for duanzi  ; item[3] for vote number
				pageStories.append([item[0].strip(), text.strip(), item[3].strip()])
		return pageStories

	#load page and add to list
	def loadPage(self):
		#if unread page less than 2, load a new page
		if self.enable == True:
			if len(self.stories) < 2:
				#load a new page
				pageStories = self.getPageItems(self.pageIndex)
				#save this page's duanzi
				if pageStories:
					self.stories.append(pageStories)
					#pageIndex + 1, read next page next time
					self.pageIndex += 1
	#use this function, print one duanzi one time
	def getOneStory(self, pageStories, page):
		#lookthrough all the duanzi in this page
		for story in pageStories:
			#wait for user's input 
			input = raw_input()
			#input once, load page or not
			self.loadPage()
			#if input is "Q" end the function
			if input == "Q":
				self.enable = False
				return
			print u"page: %d\tauthor:%s\tvote:%s\n%s" %(page, story[0],story[2],story[1])
	#start function
	def start(self):
		print u"loading qiushibaike, press Enter for new duanzi , Q for quit"
		#enble
		self.enable =  True
		#load one page first
		self.loadPage()
		#current page
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				#get one page's duanzi
				pageStories = self.stories[0]
				#nowPage + 1
				nowPage += 1
				#del the first element for have read out 
				del self.stories[0]
				#output this page's duanzi
				self.getOneStory(pageStories, nowPage)

spider = QSBK()

spider.start()
		