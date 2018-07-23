import urllib
import urllib2

url = 'http://www.sever.com/login'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5 Windows NT)'
refer = 'http://www.zhihu.com/articles'
values = {'username': 'yueyue', 'password':'a012856'}
headers = {'User-Agent' : user_agent, 'Refer' : refer}

data = urllib.urlencode(values)
request = urllib2.Request(url, data, headers)
response = urllib2.urlopen(request)
page = response.read()
