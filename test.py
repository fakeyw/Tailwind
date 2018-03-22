import asyncio
import time
@asyncio.coroutine
def async1():
	for i in range(5):
		print("Hello1")
		r = yield from asyncio.sleep(2)
		tasks.append(async2)
	
@asyncio.coroutine
def async2():
	for i in range(5):
		print("Hello2")
		r = yield from asyncio.sleep(5)
		
@asyncio.coroutine
def async3():
	for i in range(5):
		print("Hello3")
		r = yield from asyncio.sleep(5)
	
loop=asyncio.get_event_loop()
tasks=[async1(),async2()]
loop.run_until_complete(asyncio.wait(tasks))