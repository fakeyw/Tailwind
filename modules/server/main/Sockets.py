from base.tiny_Q import QPOOL
import threading
import socket
__LOCK__ = threading.Lock()

class Socket_thread(threading.Thread): #Socket not work in main thread
	def __init__(self,socketobj,callback,host="127.0.0.1",port=8989,max_conn=1000,*args,**kw):
		print(" Binding %s:%s" % (host,port))
		self.host = host
		self.port = port
		self.max_conn = max_conn
		self.socket = socketobj
		self.callback = callback #What to do after accepted
		super(Socket_thread,self).__init__(*args,**kw)
		self.__STOP__ = False
		
	def stop(self):
		self.__STOP__ = True
		
	def run(self):
		self.socket.bind((self.host,self.port))
		self.socket.listen(self.max_conn)
		while True:
			sock, addr = self.socket.accept()
			self.callback(sock,addr)	#put into accepted_queue

#Manager of main socket and acceptions 
class Socket_layer(object):
	def __init__(self):
		self.Qs = QPOOL()
		self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.accepted_queue = self.Qs.createQ(name="acq",max_len=1000)
		self.socket_thread = None
		
	def run(self,**kw):
		self.socket_thread = Socket_thread(self.main_socket,self.sock_callback,**kw) #Start main socket
		self.socket_thread.start()
	
	#Give socket thread
	def sock_callback(self,sock,addr):
		func=self.accepted_queue.put
		accepted = [sock,addr]
		__LOCK__.acquire()
		func(accepted)
		__LOCK__.release()
		
	def stop(self):
		self.socket_thread.stop()
		
	def get_accepted_sock(self): #give raw socks to next layer
		try:
			sock = self.accepted_queue.get()
			return sock
		except Exception as e:
			return None
			
			
			