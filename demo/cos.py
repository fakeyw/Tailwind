import pika
from datetime import datetime

params=pika.URLParameters('amqp://fakeyw:config.msc@115.159.113.45:5672/%2F')
conn=pika.BlockingConnection(params)

channel=conn.channel()

unrname=str(int(datetime.now().timestamp()*1000000))
channel.queue_declare(queue=unrname)
channel.queue_bind(queue=unrname,exchange='public_v',routing_key='room-public',arguments=None)

#Special structure
def callback(ch, method, properties, body):
	#print("ch:",ch,"method:",method,"properties:",properties)
	print("[x] Received %r" % body)

channel.basic_consume(callback,queue=unrname,no_ack=True)
print("Recving")
channel.start_consuming()