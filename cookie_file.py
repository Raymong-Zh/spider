import cookielib
import urllib2

#set the file for saving cookie
filename = 'cookie.txt'
#announce a MozillaCookieJar object to save cookie and write to the file
cookie = cookielib.MozillaCookieJar(filename)
#create cookie handler by HTTPCookieProcessor in urllib2
handler = urllib2.HTTPCookieProcessor(cookie)
#create opener by handler
opener = urllib2.build_opener(handler)
#open a request
response = opener.open("http://www.baidu.com")
#save to cookie file
cookie.save(ignore_discard=True, ignore_expires=True)
