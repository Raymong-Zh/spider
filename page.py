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

	#get current date
	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d', time.localtime(time.time()))
	#get current time
	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

	#get page code by url
	def getPageByURL(self, url):
		try:
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			return response.read().decode("utf-8")
		except urllib2.URLError,e:
			if hasattr(e, "code"):
				print self.getCurrentTime(), "get question page failed, error code is", e.code
				return None
			if hasattr(e, "reason"):
				print self.getCurrentTime(), "get question page failed, reason:", e.reason
				return None
	#get text
	def getText(self, html):
		if not type(html) is types.StringType:
			html = str(html)
		#get <pre> label's content
		pattern = re.compile('<pre.*?>(.*?)</pre>', re.S)
		match = re.search(pattern, html)
		#if match oK
		if match:
			return match.group(1)
		else:
			return None
	#get best ans info
	def getGoodAnswerInfo(self, html):
		pattern = re.compile('"answer_tip.*?<a.*?>(.*?)</a>.*?<span class="time.*?>.*?\|(.*?)</span>', re.S)
        match = re.search(pattern, html)
        #if match, return ans anthor and time
        if match:
        	time = match.group(2)
        	time_pattern = re.compile('\d{2}\-\d{2}\-\d{2}', re.S)
        	time_match = re.search(time_pattern, time)
        	if not time_match:
        		time = self.getCurrentDate()
        	else:
        		time = "20" + time
        	return [match.group(1), time]
        else:
        	return [None, None]

    #get best ans
    def getGoodAnswer(self, page):
    	soup = BeautifulSoup(page)
    	text = soup.select("div.good_point div.answer_text pre")
    	if len(text) > 0:
    		#get best ans's content
    		ansText = self.getText(str(text[0]))
    		ansText = self.zhishitool.replace(ansText)
    		#get ans author
    		info = soup.select("div.good_point div.answer_tip")
    		ansInfo = self.getGoodAnswerInfo(str(info[0]))
    		#join to be a list
    		answer = [ansText, ansInfo[0], ansInfo[1], 1]
    		return answer
    	else:
    		return None
    #get ans author, ans time
    def getOtherAnswerInfo(self, html):
    	if not type(html) is types.StringType:
    		html = str(html)
    	pattern = re.compile('"author_name.*?>(.*?)</a>.*?answer_t">(.*?)</span>', re.S)
    	match = re.search(pattern, html)
    	#get ans author and ans time
    	if match:
    		time = match.group(2)
    		time_pattern = re.search(time_pattern, time)
    		time_match = re.search(time_pattern, time)
    		if not time_match:
    			time = self.getCurrentDate()
    		else:
    			time = "20" + time
    		return [match.group(1), time]
    	else:
    		return [None, None]
   	#get other answers
   	def getOtherAnswers(self, page):
   		soup = BeautifulSoup(page)
   		results = soup.select("div.question_box li.clearfix .answer_info")
   		#answers to be  a list of lists
   		for result in results:
   			#get ans content
   			ansSoup = BeautifulSoup(str(result))
   			text = ansSoup.select(".answer_txt span pre")
   			ansText = self.getText(str(text[0]))
   			ansText = self.zhishitool.replace(ansText)
   			#get ans author and time
   			info = ansSoup.select(".answer_tj")
   			ansInfo = self.getOtherAnswerInfo(info[0])
   			#combine to be a list
   			answer = [ansText, ansInfo[0], ansInfo[1], 0]
   			#append to answers
   			answers.append(answer)
   		return answers
   	#main function
   	def getAnswer(self, url):
   		if not url:
   			url = "http://iask.sina.com.cn/b/gQiuSNCMV.html"
   			page = self.getPageByURL(url)
   			good_ans = self.getGoodAnswer(page)
   			other_ans = self.getOtherAnswers(page)
   			return [good_ans, other_ans]
   			