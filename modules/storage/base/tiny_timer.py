from datetime import datetime
class timer(object):
	def __init__(self):
		self.start_time = 0
		self.end_time = 0
		
	def start(self):
		self.start_time = datetime.now().timestamp()
	
	#Not reset start_time
	def check(self):
		return datetime.now().timestamp()-self.start_time
	
	#reset start_time
	def end(self):
		time = datetime.now().timestamp()
		duration = time-self.start_time
		self.start_time = time
		return duration