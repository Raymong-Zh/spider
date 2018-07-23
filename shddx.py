__author__ = 'Raymond'
#-*-coding:utf-8-*-
import urllib
import urllib2
import socket
import types
import time
import re
import os
import subprocess

class Login:
	"""docstring for Login"""
	def __init__(self):
		#username and password
		self.username = '201200131012'
		self.password = 'XXXXXX'
		self.ip_pre = '211.87'
		#overtime of login status
		self.overtime = 720
		#check once every 10 seconds
		self.every = 10
	def login(self):
		print self.getCurrentTime(),u"trying to connect QLSC_ST wifi"
		ip = self.getIP()
		data = {
			"username" : self.username,
			"password" : self.password,
			"serverType" : "",
			"isSavePass" : "on",
			"Submit1" : "",
			"language" : "Chinese",
			"ClientIP" : self.getIP(),
			"timeoutvalue" : 45,
			"heartbeat" : 240,
			"fastwebornot" : False,
			"StartTime" : self.getNowTime(),
			#dura time
			"shkOvertime" : self.overtime,
			"strOSName" : "",
			"iAdptIndex" : "",
			"strAdpName" : "",
			"strAdptStdName" : "",
			"strFileEncoding" : "",
			"PhysAddr" : "",
			"bDHCPEnabled" : "",
			"strIPAddrArray" : "",
			"strMaskArray" : "",
			"strMask" : "",
			"iDHCPDelayTime" : "",
			"iDHCPTryTimes" : "",
			"strOldPrivateIP" : self.getIP(),
			"strOldPublicIP" : self.getIP(),
			"strPirvateIP" : self.getIP(),
			"PublicIP" : self.getIP(),
			"iPCONFIG" : 0,
			"sHttpPrefix" : "http://192.168.8.10",
			"title" : "CAMS Portal"
		}
		#message headers
		headers = {
			"User-Agent" : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
			"Host" : '192.168.8.10',
			"Origin" : 'http://192.168.8.10',
			"Referer" : 'http://192.168.8.10/portal/index_default.jsp?Language=Chinese'

		}
		post_data = urllib.urlencode(data)
		login_url = "http://192.168.8.10/portal/login.jsp?Flag=0"
		request = urllib2.Request(login_url, post_data, headers)
		response = urllib2.urlopen(request)
		result = response.read(),decode('gbk')
	#get login result
		def getLoginResult(self, result):
			if u"用户上线成功" in result:
				print self.getCurrentTime(),u"用户上线成功，在线时长为", self.overtime/60,"分钟"
			elif u"您已建立了连接" in result:
				print self.getCurrentTime(),u"您已建立了连接，无需重复登录"
			elif u"用户不存在" in result:
				print self.getCurrentTime(),u"用户不存在，请检查学号是否正确"
			elif u"用户密码错误" in result:
				pattern = re.compile('<td class="tWhite">.*?2553:(.*?)</b>.*?</td>', re.S)
				res = re.search(pattern, result)
				if res:
					print self.getCurrentTime(), res.group(1),u"请重新修改密码"
			else:
				print self.getCurrentTime(),u"未知错误,请检查学号密码是否正确"
	def getNowTime(self):
		return str(int(time.time())) + "000"

	def getIP(self):
		local_iP = socket.gethostbyname(socket.gethostname())
		if self.ip_pre in str(local_iP):
			return str(local_iP)
		ip_lists = socket.gethostbyname_ex(socket.gethostname())

		for ip_list in ip_lists:
			if isinstance(ip_list, list):
				for i in ip_list:
					if self.ip_pre in str(i):
						return str(i)
			elif type(ip_list) is types.StringType:
				if self.ip_pre in ip_list:
					return ip_list
	#check current network status
	def canConect(self):
		fnull = open(os.devnull, 'w')
		result = subprocess.call('ping www.baidu.com', shell = True, stdout = fnull, stderr = fnull)
		fnll.close()
		if result:
			return False
		else:
			return True
	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

	def main(self):
		print self.getCurrentTime(), u"您好，欢迎使用模拟登录系统"
		while True:
			nowIP = self.getIP()
			if not nowIP:
				print self.getCurrentTime(), u"请检查是否正常连接QLSC_STU wifi"
			else:
				print self.getCurrentTime(), u"成功连接了QLSC_STU wifi,本机IP为",nowIP
				self.login()
				while True:
					can_connect = self.canConect()
					if not can_connect:
						nowIP = self.getIP()
						if not nowIP:
							print self.getCurrentTime(),u"当前掉线，请确保连接上了QLSC_STU网络"
						else:
							print self.getCurrentTime(),u"当前已掉线，正在尝试重新连接"
							self.login()
					else:
						print self.getCurrentTime(), u"当前网络连接正常"
					time.sleep(self.every)
			time.sleep(self.every)

login = Login()
login.main()



		
