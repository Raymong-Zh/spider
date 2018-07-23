__author__ = 'Raymond'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re

#class for dealing with useless label
class Tool:
	#remove img label and 7bytes long space
	removeImg = re.compile('<img.*?>| {7}')
	#remove link <a> label
	removeAddr = re.compile('<a.*?>|</a>')
	#repalce to \n
	replaceLine = re.compile('<tr>|<div>|</div></p>')
	#replace to \t
	replaceTD = re.compile('<td>')
	#repalce to \n + 2 spaces
	replacePara = re.compile('<p.*?>')
	#replace br to \n
	replaceBR = re.compile('<br><br>|<br>')
	#remove other labels
	removeExtraTag = re.compile('<.*?>')

	def replace(self, x):
		x = re.sub(self.removeImg, "", x)
		x = re.sub(self.removeAddr,"", x)
		x = re.sub(self.replaceLine,"\n", x)
		x = re.sub(self.replaceTD, "\t", x)
		x = re.sub(self.replacePara, "\n  ", x)
		x = re.sub(self.replaceBR, "\n", x)
		x = re.sub(self.removeExtraTag, "", x)
		#strip()
		return x.strip()


#baidutieba class
class BDTB(object):
	"""docstring for BDTB"""
	#init function: baseurl and seeLZ as references
	def __init__(self, baseUrl, seeLZ, floorTag):
		self.baseURL = baseUrl
		self.seeLZ = '?see_lz='+str(seeLZ)
		self.tool = Tool()
		#file
		self.file = None
		#floor
		self.floor = 1
		#default title
		self.defaultTitle = u'baidutieba'
		#floor tab
		self.floorTag = floorTag


	#input pageNum, get this page's code
	def getPage(self, pageNum):
		try:
			url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			content = response.read().decode('utf-8')
			return content
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"fail to connect baidutieba,reason:", e.reason
				return None
	def getTitle(self, page):
		pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
		result = re.search(pattern, page)
		if result:
			# print result.group(1) #test output
			return result.group(1).strip()

		else:
			return None
	def getPageNum(self, page):
		pattern = re.compile('<span class="red">(.*?)</span>',re.S)
		result = re.search(pattern, page)
		if result:
			#print result.group(1) #test output
			return result.group(1).strip()
		else:
			return None
	def getContent(self, page):
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
		items = re.findall(pattern, page)
		contents = []
		for item in items:
			content = "\n" + self.tool.replace(item) + "\n"
			contents.append(content.encode('utf-8'))
		return contents

	def setFileTitle(self, title):
		#title is not None, get title OK
		if title is not None:
			self.file = open(title + ".txt", "w+")
		else:
			self.file = open(self.defaultTitle + ".txt", "w+")

	def writeData(self, contents):
		#write to file
		for item in contents:
			if self.floorTag == '1':
				floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------------------\n"
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print "url is useless, please retry"
			return
		try:
			print "this article has " + str(pageNum) + "pages"
			for i in range(1, int(pageNum)+1):
				print "writing No." + str(i) +"page's data"
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		#if error
		except IOError, e:
			print "IO error, reason" + e.message
		finally:
			print "write OK"



print u"input article code?"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("only see lz: 1 for yes, 0 for no\n")
floorTag = raw_input("write floor info or not: 1 for yes, 0 for no\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()








		