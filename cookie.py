import urllib2
import cookielib
#annouce a CookieJar object to save cookie
cookie = cookielib.CookieJar()
#create cookie handler by HTTPCookieProcessor in urllib2
handler = urllib2.HTTPCookieProcessor(cookie)
#create opener by handler
opener = urllib2.build_opener(handler)
#open request by opener like urlopen
response = opener.open('http://www.baidu.com')

for item in cookie:
	print 'Name = ' +item.name 
	print 'Value = ' +item.value

