#!/usr/bin/python3
import pika
import paho.mqtt.client as mqtt 
import json
import time
from datetime import datetime

def envoiMessage(msg):
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.4'))
	channel = connection.channel()

	channel.queue_declare(queue='accident')
	channel.basic_publish(exchange='', routing_key='accident', body=msg)

	print(" Message parti ")

	connection.close()

# fonction associées
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("/tampon")

def on_message(client, userdata, msg):
        msg_receipt = str(msg.payload.decode())
        print(" message : {} ".format(msg_receipt))
        envoiMessage(msg_receipt)

client = mqtt.Client()
client.connect("192.168.1.3",1883,60)

# callbacks
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

