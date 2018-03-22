'''MANAGER of CONNECTIONS'''
'''
To control single used source pool
'''
from random import randint
from base.tiny_Q import QPOOL
from base.tiny_SID_gene import getSID
from base.tiny_timer import timer
from time import sleep
from math import sqrt

import threading
__lock__ = threading.Lock()

#Actively add more source when pressure up
#auto_control = True
#add_source = [func,{k:v...}] 
class source_manager(object):
	def __init__(self,raw_pool,auto_control=False,add_source=None,timeout=30,interval=0.01):
		self.pool = raw_pool
		self.Qs = QPOOL() 	
		self.WQ = self.Qs.createQ('Waiting',max_len=1000)
		self.PQ = self.Qs.createQ('Prepared_source',max_len=len(raw_pool))
		self.judged_source = dict()
		self.timeout = timeout
		self.interval = interval	
		self.threads = []
		self.add_more_source = add_source
		self.auto_control = auto_control
		
		for c in self.pool: 
			self.PQ.put(c)
			
		self.start_judge_thread()
		
	def start_judge_thread(self):
		nums = len(self.pool)
		for i in range(int(sqrt(nums))):
			self.threads.append(Judge_thread(self)) 
		for t in self.threads:
			t.start()
			pass
	
	#Wanna Feature:
	#When spare for a long time STOP most threads
	#Inspire by requests
	def pressure_up(self):
		self.pool.append(self.add_more_source[0](**self.add_more_source[1]))
		t = self.threads.append(Judge_thread(self))
		t.start()
		
	def pressure_down(self):
		thread_for_stop = self.threads.pop(0)
		thread_for_stop.stop()
		
	def get_source(self):
		SID = getSID(randint(0,0xffffff))
		self.WQ.put(SID)
		T=timer()
		T.start()
		while True:
			if T.check() >= self.timeout:
				__lock__.acquire()
				self.WQ.delete(SID)
				__lock__.release()
				break
			if SID in self.judged_source:
				__lock__.acquire()
				source = self.judged_source.pop(SID)
				__lock__.release()
				return Rcall_source(source,self)
			else:
				sleep(self.interval)
		
	def return_source(self,source):
		self.PQ.put(source)
		
	def stop_judge(self):
		for t in self.threads:
			t.stop()
		

class Rcall_source(object):
	def __init__(self,source,manager):
		self.source = source
		self.manager = manager
		
	def __enter__(self):
		return self.source
		
	def __exit__(self,a,b,c):
		self.close()
		
	def close(self):
		#print('Return source')
		self.manager.return_source(self.source)
			
class Judge_thread(threading.Thread):
	def __init__(self,manager,*args,**kw):
		self.__stop__ = False
		self.manager = manager
		super(Judge_thread,self).__init__(*args,**kw)
		
	def run(self):
		#print("Judgement start working")
		while True:
			__lock__.acquire()
			ea = self.manager.PQ.is_empty()
			eb = self.manager.WQ.is_empty()
			#print(self.manager.WQ.show())
			if ea == False and eb == False:
				SID = self.manager.WQ.get()
				source = self.manager.PQ.get()
				#print(SID,source)
				self.manager.judged_source[SID] = source
			__lock__.release()
			if self.__stop__:
				break
	
	def stop(self):
		self.__stop__ = True
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		