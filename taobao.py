__author__ = 'Raymond'
# -*- coding: utf-8 -*-

import urllib
import ulllib2
import cookielib 
import re
import webbrowser

#simu login taobao
class Taobo(object):
	"""docstring for Taobo"""
	def __init__(self):
		#login url of taobao
		self.loginURL = "https://login.taobao.com/member/login.jhtml"
		#proxy ip 
		self.proxyURL = 'http://120.193.146.97:843'
		#headers when post message
		self.loginHeaders = {
			'Host':'login.taobao.com',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
			'Referer':'https://login.taobao.com/member/login.jhtml',
			'Content-Type':'application/x-www-form-urlencoded',
			'Connection':'Keep-Alive'
		}
		#username
		self.username = 'yueyue_freedom@163.com'
		#ua string, cal result of taobao algori, including timestamp,browser,screen ,random number,mouse moving, mouse click,keyboard input and so on
		self.ua = '110#5WZkAUkfkZ8AdWqC3KR7Muy22MnSZMI84NrsNTrKkPeWGK2qDwyr82ykoRCXkck84KkkHL8kc2X829muGxsZ2Ucxhed/jIpOguBN81GOyUOUwCFy8vKakKfqNazfsn9bkwmHKo6CmF6khQ7/8grfxMCIbRjIuu+DrDNcIVx9g2viq539GhXSwHpwehU3oRyzCIVFr2mssAkwsziwmq85j9cwkP5ysLgwtLx44ijOmHvwDxZUBQV5jVIQjUJhD9Nws9kkkcIXsRkis47aqHSisqrikk23sOlqsTT4tSSQBcstbUT4EKhdG9HD2i9w7NcwBy7zrBDpJdd2h2i5UCPVaOe51mygItiyT2f6PuovKdU/uiEYFJKVQFk3YYmRihysgfgnHHcXnYFdVdif8VkpwZEVR5pT6E8oWr7mcEXIBccWD52B+YP88Rz53YjXrW9I9ZmgKUK8WHcu36c19W/MaxHXcYyT06+bZnBmztt0LBGKDNuaSg7ObqkjNwwg87CMCX6riVsLjEvNmSRTyv9VxNEStSvhDXgo6cs8fh++BQcAabmGvPPYDZPFf1PuZ4UmLK40s9SzvVwYw3FxXlWiOnQghBaRj97kY9D49DviUnsxPAerCLiHpfX+1XFk43DVonNtLa5DDNPNUI60LDqrVx1R+sKH/Tae9PJToD3eFXqvXcrdyAc/5aITP71OiIabY3PO2kGZI2jfTw5hx7iuRnGu971aaC1799of2P3kr5oXW6AanswbbbFHPazYvD0Vz9RN54cK7Q+O8YOIRGXhfvlY2U=='
		#password
		self.password2 = '4f50c93b64bfe9d303af1d28feecaad9e8771cda38064624019a2034eac837a726ced532f3b29a2a133ae573ced4bf9e6f6578bcae1b646e99cbee979ce25265383cb8242917c7bb2af901d499f02a537a54e35b5b73f278c75be6d6c565ea3d2bcd58904f11bb24e6f762c48b3ec6cf1392d288708a8c825b19ccbe9b0be37c'
		
		self.post = post = {
			'ua' : self.ua,
			'TPL_checkcode' : '',
			'CtrlVersion' : '1,0,0,7',
			'TPL_password' : '',
			'TPL_redirect_url' : 'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
			'TPL_username' : self.username,
			'loginsite' : '0',
			'newlogin' : '0',
			'from' : 'tb',
			'fc' : 'default',
			'style' : 'default',
			'css_style' : '',
			'tid' : 'XOR_1_000000000000000000_625CCADDEEOOOEJJJ66423',
			'support' : '000001',
			'loginType' : '4',
			'minititle':'',
			'minipara':'',
			'umto':'NaN',
			'pstrong':'2',
			'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
		}
		#encode post data
		self.postData = urllib.urlencode(self.post)
		#proxy setting
		self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
		#cookie setting
		self.cookie = cookielib.LWPCookieJar()
		#cookie handler
		self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
		#opener setting
		self.opener = urllib2.build_opener(self.cookieHandler, self.proxy, urllib2.HTTPHandler)
	
	#need IdenCode or not
	def needIdenCode(self):
		#create request for first try
		request = urllib2.Request(self.loginURL, self.postData, self.loginHeaders)
		#response for first try
		response = self.opener.open(request)
		#get content
		content = response.read().decode('gbk')
		#get code 
		status = response.getcode()
		#if status code is 200, ok
		if status == 200:
			print u"request sucess"
			##\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801 are utf-8 code of "请输入验证码"
			pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
			result = re.search(pattern, content)
			#if search sucess, it needs IdenCode
			if result:
				print u"you need to input IdenCode"
				return content
			#or need not
			else:
				print u"you don't need to input IdenCode"
				return False
		else:
			print u"request fail"
	#get IdenCode img
	def getIdenCode(self, page):
		#get IdenCode img
		pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
		#match result
		matchResult = re.search(pattern, page)
		#match Ok
		if matchResult and matchResult.group(1):
			print matchResult.group(1)
			return matchResult.group(1)
		else:
			print u"no IdenCode content"
			reutrn False
	#input IdenCode, request again
	def loginWithIdenCode(self):
		#remind user to input IdenCode
		IdenCode = raw_input('please input IdenCode:')
		#add the IdenCode to post data
		self.post['TPL_checkcode'] = IdenCode
		#encode post data again
		self.postData = urllib.urlencode(self.post)
		try:
			#request again
			request = urllib2.Request(self.loginURL, self.postData, self.loginHeaders)
			#get response
			response = self.opener.open(request)
			#get content
			content = response.read().decode('gbk')
			#check if IdenCode error \u9a8c\u8bc1\u7801\u9519\u8bef "验证码错误"
			pattern re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef', re.S)
			result =re.search(pattern, content)
			#if content includes "验证码错误"
			if result:
				print u"IdenCode error"
				return False
			else:
				#if result concludes J_HToken, it is input right IdenCode
				tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
				tokenMatch = re.search(tokenPattern, content)

				#if match OK
				if tokenMatch:
					print u"right IdenCode"
					print tokenMatch.group(1)
					return tokenMatch.group(1)
				else:
					#match fail, fail to get J_HToken
					print u"fail to get J_HToken"
					return False
		except urllib2.HTTPError, e:
			print u"connection error, reason:", e.reason
			reutrn False




	#get st by token
	def getSTbyToken(self, token):
		tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token
		request = urllib2.Request(tokenURL)
		response = urllib2.urlopen(request)
		#process st, get loginURL
		pattern = re.compile('{"st":"(.*?)"}', re.S)
		result = re.search(pattern, response.read())
		#if match OK 
		if result:
			print u"get st OK "
			st = result.group(1)
			return st
		else:
			print u"can't find st"
			return False


	#login by st code
	def loginByST(self, st, username):
		stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st,username)
		headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host':'login.taobao.com',
            'Connection' : 'Keep-Alive'
        }
        request = urllib2.Request(stURL, headers = headers)
        response = self.newOpener.open(request)
        content = response.read().decode('gbk')
        pattern = re.compile('top.location = "(.*?)"', re.S)
        match = re.search(pattern, content)
        if match:
        	print u"login OK"
        	location = match.group(1)
        	return True 
        else:
        	print u"fail to login"
        	return False


	#getGoodsPage
	def getGoodsPage(self, pageIndex):
		goodsURL = 'http://buyer.trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1&pageNum=' + str(pageIndex)
		response = self.newOpener.open(goodsURL)
		page = response.read().decode('gbk')
		return page


	#获取所有已买到的宝贝信息
    def getAllGoods(self,pageNum):
        print u"获取到的商品列表如下"
        for x in range(1,int(pageNum)+1):
            page = self.getGoodsPage(x)
            self.tool.getGoodsInfo(page)

    	#main function
	def main(self):
		#need IdenCode or not
		needResult = self.needIdenCode()
		if not needResult == None:
			if not needResult == False:
				print u"you need input IdenCode"
				idenCode = self.getIdenCode(needResult)
				#link to IdenCode
				if not idenCode == False:
					print u"get IdenCode Ok"
					print u"input IdenCode in browser"
					webbrowser.open_new_tab(idenCode)
					J_HToken = self.loginWithIdenCode()
					print "J_HToken", J_HToken
				#fail IdenCode
				else:
					print u"fail to get IdenCode, please retry"
			else:
				print u"no need to input IdenCode"
		else:
			print u"request to login fail, unkown need IdenCode or not"


		#判断token是否正常获取到
        if not self.J_HToken:
            print "获取Token失败，请重试"
            return
        #获取st码
        st = self.getSTbyToken(self.J_HToken)
        #利用st进行登录
        result = self.loginByST(st,self.username)
        if result:
            #获得所有宝贝的页面
            page = self.getGoodsPage(1)
            pageNum = self.tool.getPageNum(page)
            self.getAllGoods(pageNum)
        else:
            print u"登录失败"


taobao = Taobo()
taobao.main()


		
