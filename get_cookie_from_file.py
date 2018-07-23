import cookielib
import urllib2

#create MozillaCookieJar object
cookie = cookielib.MozillaCookieJar()
#read cookie from file
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
#create request
req = urllib2.Request('http://www.baidu.com')
#create an opener by build_opener function in urllib2
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

response = opener.open(req)
print response.read()

