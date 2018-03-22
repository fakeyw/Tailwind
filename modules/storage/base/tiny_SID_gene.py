from datetime import datetime
import hashlib

def getSID(simple_pattern):
	pattern=simple_pattern+int(datetime.now().timestamp()*100000)
	sid=hashlib.md5(str(pattern).encode('utf-8')).hexdigest()
	return sid