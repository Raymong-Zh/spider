__author__='Raymond'

#-*- coding:utf-8-*-

import urllib
import ulrlib2
import re
import retool
import os

#classs tbmm
class tbmm:
	#init
	def __init__(self):
		self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
		self.tool = retool.Tool()

	#get the index page's content
	def getPage(self, pageIndex):
		url = self.siteURL + "?page=" + str(pageIndex)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		return response.read().decode('gbk')

	#get mm info
	def getContents(self, pageIndex):
		page = self.getPage(pageIndex)
		pattern = re.compile('<div class='list-item'.*?pic_word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>', re.S)
		items = re.findall(pattern, page)
		contents = []
		for item in items:
			contents.append([item[0], item[1], item[2], item[3], item[4]])

	#get mm page info 
	def getDetailPage(self, infoURL):
		response = urllib2.urlopen(infoURL)
		return response.read().decode('gbk')
	#get brief text
	def getBrief(self, page):
		pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
		result = re.search(pattern, page)
		return self.tool.replace(result.group(1))
	#get imgs
	def getAllImg(self, page):
		pattern = re.compile('<div calss="mm-aixiu-content".*?>(.*?)<!--', re.S)
		content = re.search(pattern, page)
		patternImg = re.compile('<img.*?src"(.*?)"', re.S)
		images = re.findall(patternImg, content.group(1))
		return images

	#save images
	def saveImgs(self, images, name):
		number = 1
		print u"find", name, u"has", len(images),u"images"
		for imageURL in images:
			splitPath = imageURL.split('.')
			fTail = splitPath.pop()
			if len(fTail) > 3:
				fTail = "jpg"
				fileName = name + "/" + str(number) + "." + fTail
				self.saveImg(imageURL, fileName)
				number += 1
	#save icon
	def saveIcon(self, iconURL, name):
		splitPath = iconURL,split('.')
		fTail = splitPath.pop()
		fileName = name + "/icon." + fTail
		self.saveImg(iconURL, fileName)

	#save brief
	def saveBrief(self, content, name):
		fileName = name + "/" + name + ".txt"
		f = open(fileName, "w+")
		print u"saving her info", fileName
		f.write(conten.encode('utf-8'))

	#save a img
	def saveImg(self, imageURL, fileName):
		u = urllib2.urlopen(imageURL)
		data = u.read()
		f = open(fileName, 'wb')
		f.write(data)
		print u"saving picture", fileName
		f.close()

	#make dir
	def mkdir(self, path):
		path = path.strip()
		#check the path exists or not
		isExists = os.path.exists(path)
		if not isExists:
			print u"making dir", path, u"'s forlder"
			os.makedirs(path)
			return True
		else:
			print path, "already exists"
			return False
	#save pageinfo
	def savePageInfo(self, pageIndex):
		contents = self.getContents(pageIndex)

		for item in contents:
			print u"find a mm, name", item[2], u"age", item[3], u"she is at", item[4]
			print u"saving", item[2], "'s info"
			print u"find her site", item[0]

			detailURL = item[0]

			detailPage = self.getDetailPage(detailURL)

			brief = self.getBrief(detailPage)
			images = self.getAllImg(detailPage)
			self.mkdir(item[2])
			self.saveBrief(brief, item[2])
			self.saveIcon(item[1], item[2])
			self.saveImgs(images, item[2])

		def savePagesInfo(self, start, end):
			for i in range(start, end+1):
				print u"saving No.", i, u"sites"
				self.savePageInfo(i)


tbm = tbmm()
tbm.savePagesInfo()
