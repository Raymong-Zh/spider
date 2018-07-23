import urllib
import urllib2

values = {}
values['username'] = 'yueyue_freedom@163.com'
values['password'] = 'a012856'
data = urllib.urlencode(values)
url = "http://passport.csdn.net/account/login"
geturl = url + "?" +data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()
