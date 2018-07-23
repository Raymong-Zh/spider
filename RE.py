"""
#return pattern object
re.compile(string[,flag])
#functions for matching
re.match(pattern, string[,flags])
re.search(pattern, string[,flags])
re.split(pattern, string[,maxsplit])
re.findall(pattern, string[,flags])
re.finditer(pattern, string[, flags])
re.sub(pattern, repl, string[,count])
re.subn(pattern, repl, string[,count])
"""

__author__ = "ZYY"
# -*- coding: utf-8 -*-

#import re module
import re

#compile reg to pattern object
pattern = re.compile(r'hello')

#use re.match to match text
result1 = re.match(pattern, 'hello')
result2 = re.match(pattern, 'hello ZYY!')
result3 = re.match(pattern, 'helo ZYY!')
result4 = re.match(pattern, 'hello ZYY!')

#if 2 match success
if result1:
	#get group info
	print result1.group()
else:
	print "1 fail match"
#if 2 match success
if result2:
	#get group info
	print result2.group()
else:
	print "2 fail match"

#if 3 match success
if result3:
	#get group info
	print result3.group()
else:
	print "3 fail match"

#if 4 match success
if result4:
	#get group info
	print result4.group()
else:
	print "4 fail match"

