# -*- coding:utf-8 -*-
import re

#deal with page's lable
class Tool(object):
	"""docstring for Tool"""
	#remove hyper link adv
	removeADLink = re.compile('<div class="link_layer.*?</div>')
	#remove img lable, 1-7 bit space, &nbsp
	removeImg = re.compile('<img.*?>| {1, 7}|&nbsp;')
	#remove hyper link lable
	removeAddr = re.compile('<a.*?>|</a>')
	#replace line lable to be \n
	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
	#replace <td> lable to be \t
	replaceTD = re.compile('<td>')
	#replace br
	replaceBR = re.compile('<br><br>|<br>')
	#remove other lables
	removeExtraTag = re.compile('<.*?>')
	#remove None line
	removeNoneLine = re.compile('\n+')
	def replace(self, x):
		x = re.sub(self.removeADLink,"",x)
		x = re.sub(self.removeImg,"",x)
		x = re.sub(self.removeAddr,"",x)
		x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip() remove other info before or behind the x
        return x.strip()
