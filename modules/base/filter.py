import re
from urllib.parse import unquote,quote

#这是后端最外层的过滤
#进会过滤转码
#出会转回去 
#也就是说，显示出来的都是已经被转回的信息了
#In [str] - filter - json
class Filter(object):
	def __init__(self,raw_str):
		self.raw_str=raw_str
		
	def json_filter(self):
		raw_str=self.raw_str
		raw_str.replace("'","\'")
		raw_str.replace('"','\"')
		raw_str.replace("\n","\\n")				#maybe \n -> <br>
		raw_str.replace("\r","\\r")
		return quote(raw_str,safe="'\"")
	
	def recover(self):
		return unquote(self.raw_str)

	def xss_filter(self):
		raw_str=self.raw_str
		raw_str.replace('<','&#60;')
		raw_str.replace('>','&#62;')
		raw_str.replace('&','&#38;')
		return raw_str
	
	def sql_filter(self):
		raw_str=self.raw_str
		raw_str.replace("'","\'")
		raw_str.replace('"','\"')
		return raw_str
	