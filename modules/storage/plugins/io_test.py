import threading
from base.tiny_timer import timer

class ioTask(object):
	def __init__(self,func,*args,**kw):
		self.__COUNT__ = [0]
		self.__LOCK__ = threading.Lock()
		self.__POOL__ = []
		self.__TIMER__ = timer()
		self.io_func = func
		self.args = args
		self.kw = kw
	
	def io_test(self,repeat):
		for i in range(repeat):
			self.io_func(*self.args,**self.kw)
			self.__LOCK__.acquire()
			self.__COUNT__[0]+=1
			self.__LOCK__.release()
	
	def	start(self,threads,repeat):
		for i in range(threads):
			t=threading.Thread(target=self.io_test,args=(repeat,))
			self.__POOL__.append(t)
		print("[*]Start IO test: %s threads (%s tasks for each)" % (threads,repeat))	
		self.__TIMER__.start()
		for t in self.__POOL__:
			t.start()
		for t in self.__POOL__:	
			t.join()
		duration = self.__TIMER__.end()
		print("[*]Completed task num:",self.__COUNT__[0],",Consumed time:",duration)
	

	

