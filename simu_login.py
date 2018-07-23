import urlib
import urllib2
import cookielib

filename = 'cookie.txt'
#announce a MozillaCookieJar object to save cookie and write to file
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.encode({
	        'stuid' : '201200131012',
	        'pwd' : '23342321'
})

#login URL
loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
#simu to login, save cookie
result = opener.open(loginUrl, postdata)
#save cookie to the file
cookie.save(ignore_discard=True, ignore_expires=True)
#use cookie to visit another website for querying grade
gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjxc.curscopre'
#visit this site
result = opener.open(gradeUrl)
print result.read()
 