__author__='Raymond'
#-*- coding:utf-8-*-

import urllib
import urllib2
import re
import os

#classs tbmm
class MM:
	#init
	def __init__(self):
		self.siteURL = 'https://www.nvshens.com'
		self.cwd = os.getcwd()
		self.NO = 10

	#get  page's content
	def getPage(self, url):
		url = url
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		page = response.read().decode('utf-8')
		return page
	#get all the pgsites of a girl; one pgsite for one group of pics
	def getpgsites(self, girlpage):
		pattern = re.compile("class='igalleryli_link' href='(.*?)' >",re.S)
		pgsites = re.findall(pattern, girlpage)
		return pgsites
	#get page num of a pgsite
	def getpgPicNum(self,pgsiteindexurl):
		pgpage = self.getPage(pgsiteindexurl)
		pattern = re.compile("<a href='/g/.*?.html' >(.*?)</a>", re.S)
		result = re.findall(pattern,pgpage)
		picnum = len(result)+1
		return picnum
	#get urls in one pate
	def getImgUrls(self,pgsiteurl):
		pgpage = self.getPage(pgsiteurl)
		pattern = re.compile("<img src='(.*?)' alt='(.*?)' />", re.S)
		imgs = re.findall(pattern, pgpage)
		return imgs
	#get girl's name as dir name
	def getdirname(self, girlpage):
		pattern = re.compile('<h1 style="font-size:.*?>(.*?)</h1>', re.S)
		dirname = re.search(pattern, girlpage)
		return dirname.group(1)
	#save an img
	def saveImg(self, imageURL, fileName):
		u = urllib2.urlopen(imageURL)
		data = u.read()
		f = open(fileName, 'wb')
		f.write(data)
		print u"saving picture", fileName
		f.close()
	#make dir of a girl
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
	#save one page's imgs
	def saveOnePageImgs(self, pgsiteurl, dirname):
		pgsiteurl = pgsiteurl
		imgs = self.getImgUrls(pgsiteurl)
		for img in imgs:
			imgurl = img[0]
			imgdir = self.cwd + '\\' + dirname + '\\'
			imgname = img[1].encode('utf-8') +'.jpg'
			imgpath =  imgdir + imgname.decode('utf-8')
			self.saveImg(imgurl, imgpath)
	#save one pg's imgs
	def saveOnepgImgs(self, pgsite, dirname):
		pgsiteindexurl = self.siteURL+pgsite 
		pgPicNum = self.getpgPicNum(pgsiteindexurl)
		for i in range(1,pgPicNum+1):
			pgsiteurl = pgsiteindexurl + str(i)+ ".html"
			self.saveOnePageImgs(pgsiteurl, dirname)
	#save one person's imgs
	def saveOnePersonImgs(self, girlpage, dirname):
		pgsites = self.getpgsites(girlpage)
		#save several of pgs; num is less then NO
		if len(pgsites) < self.NO:
			for pgsite in pgsites:
				self.saveOnepgImgs(pgsite, dirname)
		else:
			for pgsite in pgsites[:self.NO]:
				self.saveOnepgImgs(pgsite, dirname)


	#get all the girls' No. in rank page
	def getgirls(self):
		rank_url = 'https://www.nvshens.com/rank/'
		girlslist = []
		rankpage = self.getPage(rank_url)
		pattern = re.compile("href='/girl/(.*?)/'", re.S)
		girls = re.findall(pattern, rankpage)
		for girl in girls:
			if girl in girlslist:
				continue
			else:
				girlslist.append(girl)
		return girlslist
	#save one girl's imgs
	def saveonegirl(self, girlnum):
		girlnum = girlnum
		girlsite = '/girl/' + girlnum + '/'
		girlalbumsite = '/girl/' + girlnum +'/album/'
		url_girlsite = self.siteURL + girlsite
		url_girlsiteall = self.siteURL + girlalbumsite
		girlpage = self.getPage(url_girlsite)
		dirname = self.getdirname(girlpage)
		self.mkdir(dirname)
		#the girl has an album or not
		pattern = re.compile('archive_more', re.S)
		ismore = re.search(pattern, girlpage)
		if not ismore :
			girlpageall = self.getPage(url_girlsite)
		else:
			girlpageall =self.getPage(url_girlsiteall)
		
		self.saveOnePersonImgs(girlpageall, dirname)
	#main function
	def main(self):
		girlslist = self.getgirls()
	
		for girl in girlslist:
			try:
				self.saveonegirl(girl)
			except UnicodeEncodeError,e:
				print e.reason

mm = MM()
mm.main()











		

"""
mm = MM()
girlsite = '/girl/22162/'
url_girlsite = mm.siteURL + girlsite
girlpage = mm.getPage(url_girlsite)
pgsites = mm.getpgsites(girlpage)

pgsite = pgsites[0]
pgsiteindexurl = mm.siteURL+pgsite 
print u"total", mm.getpgPicNum(pgsiteindexurl), "pages"

dirname = mm.getdirname(girlpage)
mm.mkdir(dirname)


pgsiteurl = pgsiteindexurl + "1.htm"
imgs = mm.getImgUrls(pgsiteurl)


for img in imgs:
	imgurl = img[0]
	cwd = os.getcwd()
	imgdir = cwd + '\\' + dirname + '\\'
	
	imgname = img[1].encode('gbk') +'.jpg'
	imgpath =  imgdir + imgname.decode('gbk') 

	mm.saveImg(imgurl, imgpath)
"""
	




