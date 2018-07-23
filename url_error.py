import urllib2
request = urllib2.Request('http://www.x124995hfeddd.com')
try:
	urllib2.urlopen(request)
except urllib2.URLError, e:
	print e.reason
