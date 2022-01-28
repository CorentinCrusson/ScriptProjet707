#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

def save_json_stat(data):
    with open('/json-save/stat.json', 'w') as outfile:
        json.dump(data, outfile)
def save_json_accident(data):
    print(data)
    with open('/json-save/accident.json', 'r') as f:
         data_json = json.load(f)
    if data['etat'] == 'en cours':
       dt_object = datetime.fromtimestamp(data['timestamp'])
       data['heure_debut'] = dt_object.strftime("%Hh%M")
       data['nb_pers'] = 1
       data_json["accidents"].append(data)
    else:
       for i,vehicule in enumerate(data_json["accidents"]):
          try:
             print(i)
             if vehicule['id_vehicule'] == data['id_vehicule']:
                #data_json["accidents"][i] = data_json["accidents"].pop(i)
                data_json["accidents"].pop(i)
          except:
             print("error")
    with open('/json-save/accident.json', 'w') as f:
         json.dump(data_json,f)

# fonction associes
def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("/web")

def on_message(client, userdata, msg):
        msg_receipt = str(msg.payload.decode())
        print(" message : {} ".format(msg_receipt))
        data_event = json.loads(msg_receipt)
        if data_event['type_msg'] == "STAT":
           save_json_stat(data_event)
        else:
           save_json_accident(data_event)

client = mqtt.Client()
client_send = mqtt.Client()

client.connect("192.168.1.3",1883,60)

# callbacks
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

