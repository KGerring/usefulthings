#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = rabbitmq_pika
# author=AutisticScreeching
# date = 3/29/17
import sys, os
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
hello_queue = channel.queue_declare(queue='hello')
task_queue = channel.queue_declare(queue='task_queue', durable=True)
pub = channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body): print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()




###### new_task.py #####
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
		                      delivery_mode=2,  # make message persistent
                      ))
##### worker.py ######
import time

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	time.sleep(body.count(b'.'))
	print(" [x] Done")

###

def callback(ch, method, properties, body):
	print(
	" [x] Received %r" % (body,))
	time.sleep(body.count('.'))
	print(
	" [x] Done")
	ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(callback,
                      queue='hello')

###### direct, topic, headers and fanout
channel.exchange_declare(exchange='logs',
                         type='fanout')
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
result = channel.queue_declare()
result = channel.queue_declare(exclusive=True)
if __name__ == '__main__': print(__file__)