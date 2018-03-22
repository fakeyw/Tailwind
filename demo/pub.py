import pika

params=pika.URLParameters('amqp://fakeyw:config.msc@115.159.113.45:5672/%2F')
conn=pika.BlockingConnection(params)

channel=conn.channel()

#when exchange='', using default ex(direct). OR queue_bind is needed
#channel.queue_bind(queue, exchange, routing_key=None, arguments=None)

#channel.basic_publish(exchange='',routing_key='room-public',body

channel.exchange_declare(exchange='public_v')
#channel.queue_declare(queue='room-public')
class pub(object):
	def __init__(self,exchange=None,routing_key=None):
		if not exchange:
			self.exchange=''
		else:
			self.exchange=exchange
		self.routing_key=routing_key
		print('ex',exchange,'rk',routing_key)
	
	def publish(self,body):
		channel.basic_publish(exchange=self.exchange,routing_key=self.routing_key,body=body)
		print('Sending to ex [%s],key [%s],as [%s]' % (self.exchange,self.routing_key,body))

pubmsg=pub(exchange='public_v',routing_key='room-public')
msg=''
while msg != 'exit':
	msg=input("MSG:")
	pubmsg.publish(msg)
	
#不能先发出再声明queue	
#channel.queue_declare(queue='room-public')
#channel.queue_delete(queue='room-public')