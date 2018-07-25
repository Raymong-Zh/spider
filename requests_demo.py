import requests

r = requests.get('http://www.baidu.com')
print type(r)
print r.status_code
print r.encoding
#print r.text
print r.cookies
