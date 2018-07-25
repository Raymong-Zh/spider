# -*- coding: utf-8 -*-
import MySQLdb
import time

class Mysql(object):
	"""docstring for Mysql"""
	def getCurrrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
	#init databse
	def __init__(self):
		try:
			self.db = MySQLdb.connect('127.0.0.1', 'root', 'root1234','iask')
			self.cur = self.db.cursor()
		except MySQLdb.Error, e:
			print self.getCurrrentTime(), "failed to connect databse, reason%d: %s" %(e.args[0], e.args[1])

	#insert data
	def insertData(self, table, my_dict):
		try:
			self.db.set_character_set('utf8')
			cols = ', '.join(my_dict.keys())
			values = '","'.join(my_dict.values)
			sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
			try:
				result = self.cur.execute(sql)
				insert_id = self.db.insert_id()
				self.db.commit()
				#execute ok or not
				if result:
					return insert_id
				else:
					return 0
			except MySQLdb.Error,e:
				self.db.rollback()
				if "key 'PRIMARY'" in e.args[1]:
					print self.getCurrrentTime(),"data already exists"
				else:
					print self.getCurrrentTime(),"insert data fail, reason %d: %s" %(e.args[0], e.args[1])
		except MySQLdb.Error,e:
			print self.getCurrrentTime(),"database Error, reason %d: %s" % (e.args[0], e.args[1])
			