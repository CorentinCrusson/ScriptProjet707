#!/usr/bin/python3
import paho.mqtt.client as mqtt

# fonction associées
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("/evenement")

def on_message(client, userdata, msg):
        msg_receipt = str(msg.payload.decode())
        print(" message : {} ".format(msg_receipt))
        print("j envoies"+str(msg_receipt))

        client.publish("/web",msg_receipt)
        if "STAT" not in msg_receipt:
            client.publish("/tampon",msg_receipt)

client = mqtt.Client()
client.connect("localhost",1883,60)

# callbacks
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever() 

