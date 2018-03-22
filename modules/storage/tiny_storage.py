import sys
import os
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from base.tiny_Q import QPOOL
from base.tiny_source_manager import source_manager
from base.tiny_SID_gene import getSID
from sqlite3 import connect
import sys
import time

sys.path.append('..')
		
#define sql service
class STORAGE(object):
	def __init__(self,type=None,username=None,passwd=None,path=None,database=None,MAX_CONN=10):
		self.MAX_CONN = MAX_CONN
		self.type = type
		self.user = username
		self.passwd = passwd
		self.path = path
		self.dbuse = database
		self.__POOL__ = self.create_pool()
		self.tables = dict() #name&class
		self.attr_dict = dict()
		self.func_dict = dict()
	
	def create_pool(self):
		#[conn,cursor]
		raw_pool = [[c,c.cursor()] for c in [connect(self.path,check_same_thread=False) for i in range(self.MAX_CONN)]]
		MPOOL = source_manager(raw_pool)
		return MPOOL
		
	def refresh(self):
		self.attr_dict = dict()
		self.func_dict = dict()
	
	def set_attr(self,name,type,default=""):
		self.attr_dict[name] = [type,default]
		
	def set_func(self,name,func):
		self.func_dict[name] = func
		
	#Construct a class of table, its instance is table's rows 
	def define(self,table_name,primary_key=None,auto=False):
		class TableMetaclass(type):	
			def __new__(cls, name, bases, attrs):
				attrs["__attrs__"] = dict() 
				attrs["__add_funcs__"] = self.func_dict
				attrs["__database__"] = self
				attrs["__table__"] = table_name
				attrs["__count__"]=[0] #count rows
				
				if primary_key == None:
					attrs["__primary_key__"] = 'TStorage_default_id'
				else:
					attrs["__primary_key__"] = primary_key
				
				#Add unique id col for every table
				attrs["__attrs__"]['TStorage_default_id'] = set_type('TStorage_default_id','str')
				
				#save attrs
				for [name,[attr_type,default]] in list(self.attr_dict.items()):
					attrs["__attrs__"][name] = set_type(name,attr_type,default=default)
					
				#save funcs
				for [name,func] in list(self.func_dict.items()):
					attrs[name] = func
				return type.__new__(cls, name, bases, attrs)

		class Table(dict,metaclass=TableMetaclass):
			def __init__(self,**kw):
			
				#attrs for pieces
				self.__count__[0] += 1
				self.TStorage_default_id = getSID(self.__count__[0])
				super(Table,self).__init__(**kw)
				
				#set default value of blank attrs
				for [name,field] in self.__attrs__.items():
					if name not in self:
						self[name]=field.default

				self.check_type()
				
				#normalize attrs for safety sql query use
				self.normalized_attrs = dict()
				for [name,field] in self.__attrs__.items():
					self.normalized_attrs[name]=field.normalize(self[name])
				
				self.update()
			
			def __str__(self):
				str = '['+self.__table__+']\n'
				for [name,field] in self.__attrs__.items():
					str+="%s[%s]\n" % (name,field.type_sql)
				return str
				
			def __getattr__(self, key):
				try:
					return self[key]
				except KeyError:
					raise AttributeError(r"Table object has no attribute '%s'" % key)

			def __setattr__(self, key, value):
				self[key] = value
				
			
			def check_type(self,target=None):
				if target == None:
					for [name,field] in self.__attrs__.items():
						if field.type_py != type(self[name]):
							raise TypeError(name)
				else:
					if self.__attrs__[target].type_py != type(self[target]):
						raise TypeError(target)
						
			def update(self):
				check_exist = self.__database__.SELECT('*').FROM(self.__table__).WHERE(TStorage_default_id = self.TStorage_default_id)
				#check_exist = self.__database__.execute("SELECT * FROM %s WHERE TStorage_default_id = %s" % (self.__table__,self.normalized_attrs['TStorage_default_id']))
				names = []
				values = []
				for [name,_] in self.__attrs__.items():
					if name != self.__primary_key__:
						names.append(name)
						values.append(self.normalized_attrs[name])
				if len(check_exist) == 0:
					names = ','.join(names)
					values = ','.join(values)
					pattern = "INSERT INTO {table} ({names}) VALUES({values})".format(table=self.__table__,names=names,values=values)
					#print(pattern)
				else:
					kv=','.join(["%s=%s" % kv for kv in zip(names,values)])
					pattern = "UPDATE {table} SET {kv}".format(table=self.__table__,kv=kv)
				self.__database__.execute(pattern)
				
			def refresh(self):#pull
				try:
					name_list = [name for (name,_) in self.__attrs__.items()]
					names = ','.join(name_list)
					res = self.__database__.execute("SELECT %s FROM %s WHERE TStorage_default_id = %s" % (names,self.__table__,self.normalized_attrs['TStorage_default_id']))
					kv={k:v for (k,v) in zip(name_list,res[0])}
					self.change(**kv)
					return True
				except Exception as e:
					print(e)
					return False
					
			def change(self,**kw):
				for k,v in kw.items():
					try:
						self[k]=v
					except Exception as e:
						print(e)
					self.check_type(target=k)
					self.normalized_attrs[k]=self.__attrs__[k].normalize(v)
			
			#delete itself
			def delete(self):
				pass
			
			def get_info(self,name):
				self.refresh()
				return getattr(self,name,self.__attrs__[name].default)
			
			def all_info(self):
				self.refresh()
				attrs=dict()
				for name,field in self.__attrs__.items():
					a,b,c=name,field.type_sql,getattr(self,name,field.default)
					attrs[a]=[b,c]
				return attrs
		
		#Construction complete
		self.tables[table_name] = Table
		result = self.create_table(Table,auto=auto)
		if result != True:
			print("Operation failed, name repeated : %s" % table_name)
		
		return Table
		
	def create_table(self,Table,auto=False):
		#get table info from Class attr
		attrs = list(Table.__attrs__.items())
		primary_key = Table.__primary_key__
		params = list()
		table_name = Table.__table__
		for [name,field] in attrs:
			piece="%s %s" % (name,field.type_sql)
			if name == primary_key:
				piece += " PRIMARY KEY"
				if auto :
					piece += " AUTOINCREMENT"
			params.append(piece)
		
		params=",".join(params)
		pattern_table = "CREATE TABLE %s (%s)" % (table_name,params)
		try:
			self.execute(pattern_table)
		except Exception as e:
			print("In create_table",e)
			return False
			
		return True
	
	#For persistence
	def load_tables(self):
		pass
	
	def save_tables(self):
		pass
		
	#create loaded tables
	def create_all(self):
		pass
		
	def execute(self,cmd):
		with self.__POOL__.get_source() as source:
			result = source[1].execute(cmd).fetchall()
			source[0].commit()
		return result
		
	def SELECT(self,args):
		return query_select_layer(self,*args)
		
	def list_all(self,name):
		pass
					
	def delete(self,table_name):
		pass
		

class query_select_layer(object):
	def __init__(self,db,*args):
		self.select = ["SELECT",','.join([i for i in args])]
		self.db = db
		
	def FROM(self,table_name):
		return query_from_layer(self.db.tables[table_name],self.select)
	
class query_from_layer(object):
	def __init__(self,table,select):
		self.table = table
		self.select = select
		self.From = ["FROM %s" % table.__table__]
	
	def WHERE(self,**kw):
		if len(kw) == 0:
			where = ''
		else:
			where = ["WHERE"] + ["\"%s\"=\"%s\"" % kv for kv in kw.items()]
		query = ' '.join(self.select+self.From+where)
		result = self.table.__database__.execute(query)
		return result

'''Fields for mapping'''
class type_field(object):
	def __init__(self,name,type_sql,type_py,default):
		self.name = name
		self.type_sql = type_sql
		self.type_py = type_py
		self.default = default
		
	def __str__(self):
		return "[%s:%s]" % (self.__class__.__name__,self.name)

	
class type_int(type_field):
	def __init__(self,name,default):
		if default == '':
			default = 0
		super(type_int,self).__init__(name,type_sql="integer",type_py=type(int()),default=default)
		
	def normalize(self,i):
		return str(i)
	
class type_str(type_field):
	def __init__(self,name,default):
		if default == '':
			default = ''
		super(type_str,self).__init__(name,type_sql="varchar",type_py=type(str()),default=default)
	
	def normalize(self,s):
		return "\"%s\"" % s

fields={"int":type_int,"str":type_str}

def set_type(name,type,default=''):
	return fields[type](name,default)
	

