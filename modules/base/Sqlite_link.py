from sqlite3 import connect
import sys

conn=connect('blog.db',check_same_thread = False)
cursor=conn.cursor()

class sql_handler(object):
	def __init__(self,filename):
		self.conn=connect(filename,check_same_thread=False)
		self.cursor=self.conn.cursor()
	'''---------------------------------------
	table	 	str		single
	colomns 	list	muti
	knv 		dict	muti/none
	btw		dict	{'col':(a,b)}	a< col <b
	'''
	def select(self,table,colomns,knv=None,btw=None):
		colstr=','.join(colomns)
		if knv == None and btw == None:
			addstr=''
		else:
			addstr='WHERE'
			if knv:
				key2value=list()
				for (k,v) in list(knv.items()):
					key2value.append(' %s=\'%s\' ' % (k,v))
				addstr=addstr+'AND'.join(key2value)	# col = ?
				
			if btw:
				if addstr!='WHERE':
					addstr=addstr+' AND '
				(key,(low,high))=btw.popitem()
				addstr=addstr+' %s BETWEEN %d AND %d' % (key,low,high)	# col BETWEEN a and b
			
		pattern='SELECT %s FROM %s %s' % (colstr,table,addstr)
		print(pattern)
		#--------------------------------------------------
		try:
			raw_info=cursor.execute(pattern).fetchall()
			if not raw_info:
				return None
		except Exception as e:
			print(e)
			return None
		
		info=list()
		for pieces in raw_info:
			temp_dict=dict()
			for i in range(len(colomns)):
				temp_dict[colomns[i]]=pieces[i]
			info.append(temp_dict)
		return info
		
	'''---------------------------------
	table	 	str		single
	cnv 		dict	muti
	'''
	def insert(self,table,cnv):
		if not cnv:
			return False
		knvlist=list(cnv.items())
		klist=[]
		vlist=[]
		for (k,v) in knvlist:
			klist.append(k)
			vlist.append(v)
		kstr=','.join(klist)
		vstr=','.join(vlist)
		#patten='INSERT INTO %s (x,x,x,x,x) VALUES (x,x,x,x,x)'
		pattern='INSERT INTO %s (%s) VALUES (%S)'(table,kstr,vstr)
		try:
			self.cursor.execute(pattern)
			self.conn.commit()
			return True
		except Exception as e:
			return False
		
	'''----------------------------------
	table		str		single
	cnv			dict	muti
	knv			dict	muti
	'''
	def update(self,table,cnv=None,knv=None):
		if not cnv or not knv:
			return False
		cnvlist=[]
		for (c,v) in list(cnv.items()):
			cnvlist.append("%s=\'%s\'" %(c,v))
		cnvstr=','.join(cnvlist)
		
		knvlist=[]
		for (k,v) in list(knv.items()):
			knvlist.append("%s=\'%s\'" % (k,v))
		knvstr='WHERE %s' % ' AND '.join(knvlist)
			
		pattern='UPDATE %s SET %s %s' % (table,cnvstr,knvstr)
		#print(pattern)
		
		try:
			self.cursor.execute(pattern)
			self.conn.commit()
			return True
		except Exception as e:
			return False
	
	'''----------------------------------
	table		str		single
	knv			dict	muti
	'''
	def delete(self,table,knv):
		if not knv:
			return False
		knvlist=[]
		for (k,v) in list(knv.items()):
			knvlist.append("%s=\'%s\'" % (k,v))
		knvstr='WHERE %s' % ' AND '.join(knvlist)
		pattern="DELETE FROM %s %s" % (table,knvstr)
		#print(pattern)
		try:
			self.cursor.execute(pattern)
			self.conn.commit()
			return True
		except Exception as e:
			return False
			
	'''----------------------------------
	table		str		single
	knv			dict	muti
	'''
	def create_table(self,table)
			
blog_db=sql_handler('blog.db')
				
		