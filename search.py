#import re module
import re

#compile reg to pattern object
pattern = re.compile(r'world')

#use search() to lookup sub string
#in this example, can not  use match() to match
match = re.search(pattern, 'hello world!')

if match:
	#get group info
	print match.group()
	