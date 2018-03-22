import configparser
import sys
sys.path.append('..')

config=configparser.ConfigParser()

config.read('blog.conf')

#input aspect and a list of attr name
class Config(object):
	def __init__(self,aspect,attrs):
		self.info=dict()
		self.attrs=attrs
		for i in range(len(attrs)):
			try:
				self.info[attrs[i]]=int(config.get(aspect,attrs[i]))
			except Exception as e:
				self.info[attrs[i]]=config.get(aspect,attrs[i])
		print(self.info)
	
	def refresh(self):
		self.__init__(self)
		
	def change(conf,value):
		pass
	
	#test function
	def show(self):
		print(self.info)

#host
host_conf=Config('host',["openhost","openport","trueip"])

#general
general_conf=Config('general',["cookie_timeout"])

#authorization
l=[	"visit_index",
	"visit_articles",
	"visit_login",
	"visit_register",
	"visit_admin",
	
	"comment",
	"chatting",
	
	"get_info_basic",
	"get_info_hidden",
	"get_info_secured",
	
	"grant_communication",
	"grant_management",
	"grant_level",
	
	"admin_notice",
	"admin_comments",
	"admin_users",
	"admin_articles"	]
authorization_conf=Config('authorization',l)

#WHY not create a table?
SID={ #sql->conf
	
	'001':"visit_index"			,
	'002':"visit_articles"		,
	'003':"visit_login"			,	#fobidden without guest cookie
	'004':"visit_register"		,	#fobidden without guest cookie
	'005':"visit_admin"			,
	
	'101':"comment"				,
	'102':"chatting"			,
	
	'201':"get_info_basic"		,
	'202':"get_info_hidden"		,
	'203':"get_info_secured"	,
	
	'301':"grant_communication"	,	#about	1xx
	'302':"grant_management"	,	#about	4xx
	'303':"grant_level"			,
	
	'401':"admin_notice"		,
	'402':"admin_comments"		,
	'403':"admin_users"			,
	'404':"admin_articles"		,
	'405':"admin_pages"
}
reSID={	#conf->sql
	"visit_index":'001'			,
	"visit_articles":'002'		,
	"visit_login":'003'			,	#fobidden without guest cookie
	"visit_register":'004'		,	#fobidden without guest cookie
	"visit_admin":'005'			,
	
	"comment":'101'				,
	"chatting":'102'			,
	
	"get_info_basic":'201'		,
	"get_info_hidden":'202'		,
	"get_info_secured":'203'	,
	
	"grant_communication":'301'	,	#about	1xx
	"grant_management":'302'	,	#about	4xx
	"grant_level":'303'			,

	"admin_notice":'401'		,
	"admin_comments":'402'		,
	"admin_users":'403'			,
	"admin_articles":'404'		,
	"admin_pages":'405'
}



