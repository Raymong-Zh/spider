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

	#construct URL by page num
	def getPageURLByNum(self, page_num):
		page_url = "http://iask.sina.com.cn/c/978-all-" + str(page_num) + ".html"
		return page_url
	#get page by page num
	def getPageByNum(self, page_num):
		request = urllib2.Request(self.getPageURLByNum(page_num))
		try:
			response = urllib2.urlopen(request)
		except urllib2.URLError, e:
			if hasattr(e, "code"):
				print self.getCurrentTime(), "get page fail, error code",e.code
				return None
			if hasattr(e, "reason"):
				print self.getCurrentTime(), "get page fail, reason:", e.reason
				return None
			else:
				page = response.read().decode("utf-8")
				return page
	#get all page nums
	def getTotalPageNum(self):
		print self.getCurrentTime(), "getting page nums, please waiting"
		page =self.getPageByNum(1)
		#match the total page num \u4e0b\u4e00\u9875 is the utf-8 code of "下一页"
		pattern = re.compile(u'<span class="more".*?<span.*?<a href.*?class="">(.*?)</a>\s*<a.*?\u4e0b\u4e00\u9875</a>', re.S)
		match = re.search(pattern, page)
		if match:
			reutrn match.group(1)
		else:
			print self.getCurrentTime(), "get total page_num fail"
	#parse code of question, get author, question, num of answers and time
	def getQuestionInfo(self, question):
		if not type(question) is types.StringType:
			question = str(question)
		#print question
		pattern = re.compile(u'<span.*?question-face.*?>.*?<img.*?alt="(.*?)".*?</span>.*?<a href="(.*?)".*?>(.*?)</a>.*?answer_num.*?>(\d*).*?</span>.*?answer_time.*?>(.*?)</span>', re.S)
		match = re.search(pattern, question)
		if match:
			#get author
			author = match.group(1)
			#question link
			href = match.group(2)
			#question
			text = match.group(3)
			#num of answers
			ans_num = match.group(4)
			#ans_time
			time = match.group(5)
			time_pattern = re.compile('\d{4}\-\d{2}\-\d{2}', re.S)
			time_match = re.search(time_pattern, time)
			if not time_match:
				time = self.getCurrentDate()
			return [author, href, text, ans_num, time]
		else:
			return None
	#get all questions
	def getQuestions(self, page_num):
		#get html code
		page = self.getPageByNum(page_num)
		soup = BeautifulSoup(page)
		#get all the questions 
		questions = soup.select("div.question_list ul li")
		#look through every question
		for question in questions:
			#get question info
			info = self.getQuestionInfo(question)
			if info:
				#get question URL
				url = "http://iask.sina.com.cn" + info[1]
				#get the best answer and other questions by URL
				ans = self.page_spider.getAnswer(url)
				print self.getCurrentTime(),"finding the No.",page_num,"'s content, find a question", info[2],"ans num", info[3]
				#construnc dict of questions
				ques_dict = {
							"text" : info[2]
							"questioner" : info[0]
							"date" : info[4]
							"ans_num" : info[3]
							"url" : url
							}
				#get inserting question id (auto_incre)
				insert_id = self.mysql.insertData("iask_questions", ques_dict)
				#get the best ans
				good_ans = ans[0]
				print self.getCurrentTime(), "saving to database, the id is ", insert_id
				#if the best ans exists, intert it
				if good_ans:
					print self.getCurrentTime(), insert_id, " question has the best ans", good_ans[0]
					#construct best ans's dict
					good_ans_dict = {
									"text" : good_ans[0],
									"answer" : good_ans[1],
									"date" : good_ans[2],
									"is_good" : str(good_ans[3])
									"question_id" : str(insert_id)
									}
					#insert the best ans
					if self.mysql.insertData("iask_answers", good_ans_dict):
						print self.getCurrentTime(), "saved the best answer"
					else:
						print self.getCurrentTime(), "failed to save the best answer"
				#other answers
				other_anses = ans[1]
				#look through every answer
				for other_ans in other_anses:
					#if ans exists
					if other_ans:
						print self.getCurrentTime(), insert_id, "question has other answers", other_ans[0]
						#construct dict of other ans
						other_ans_dict = {
										"text" : other_ans[0]
										"answerer" : other_ans[1]
										"date" : other_ans[2]
										"is_good" : str(other_ans[3])
										"question_id" : str(insert_id)
										}
						#insert other ans
						if self.mysql.insertData("iask_answers", other_ans_dict):
							print self.getCurrentTime(),"saved other ans"
						else:
							print self.getCurrentTime(),"fail to save other ans"

	#main function
	def main(self):
		f_handler = open('out.log', 'w')
		sys.stdout = f_handler
		page = open('page.txt', 'r')
		content = page.readline()
		start_page = int(content.strip()) - 1
		page.close()
		print self.getCurrentTime(),"start page is ", start_page
		print self.getCurrentTime(),"spider running"
		self.total_num = self.getTotalPageNum()
		print self.getCurrentTime(), "get total index page num", self.total_num
		if not start_page:
			start_page = self.total_num
		for x in range(1, start_page):
			print self.getCurrentTime(), "parsing No.", start_page - x + 1, "'s page"
			try:
				self.getQuestions(start_page - x + 1)
			except urllib2.URLError, e:
				if hasattr(e, "reason"):
					print self.getCurrentTime(),"parse this page failed, reason:", e.reason
			except Exception,e:
				print self.getCurrentTime,"parse this page failed, reason:", e
			if start_page -x + 1 < start_page:
				f = open('page.txt', 'w')
				f.write(str(start_page - x + 1))
				print self.getCurrentTime(),"writing new code", start_page - x + 1
				f.close()
zhishi = Zhishi()
zhishi.main()



		
