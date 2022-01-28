#!/usr/bin/python3
import paho.mqtt.client as mqtt
import json
import threading, time

sauveg_vehicule = []
check_sec = 6

def supprVehicule():
    timestamp = int(time.time())
    for i,vehicule in enumerate(sauveg_vehicule):
        if vehicule['timestamp'] < timestamp-check_sec:
           sauveg_vehicule.pop(i)

def addVehicule(data):
    ok = True
    ind = 0
    for i,vehicule in enumerate(sauveg_vehicule):
       if vehicule['id_vehicule'] == data['id_vehicule']:
          ok = False
          ind = i 
    if ok is True:
       data_vehicule = {"id_vehicule": data['id_vehicule'], "vitesse": data['vitesse'], "timestamp": int(time.time())}
       sauveg_vehicule.append(data_vehicule)	 
    else:
       sauveg_vehicule[i]['vitesse'] = data['vitesse']
       sauveg_vehicule[i]['timestamp'] = int(time.time())
    
    return True

def getVitesseMoyenne():
    somme = 0
    for veh in sauveg_vehicule:
       somme = somme + veh['vitesse']
    if len(sauveg_vehicule) == 0:
       return somme
    else:
       return somme / len(sauveg_vehicule)

def updateStat(embouteillage):
    while 1:
       supprVehicule()
       data_pass = "{\"type_msg\": \"STAT\",\"vitesse_moy\": "+str(getVitesseMoyenne())+", \"nombre_vehicules\": "+str(len(sauveg_vehicule))+", \"embouteillage\": "+str(embouteillage)+"}"
       client_send.publish("/evenement", data_pass);

       #Embouteillage ?
       somme = 0
       for vehicule in sauveg_vehicule:
           if vehicule['vitesse'] < 90:
              somme = somme + 1
       if somme >= 3 :
          print("Embouteillage !!")
          embouteillage = somme
       else:
          embouteillage = 0
       time.sleep(1)

def send_msg(client_send,data_event):
    if data_event['type_msg'] == "CAM":
       addVehicule(data_event)
    else:
       data_pass = json.dumps(data_event)
       client_send.publish("/evenement", data_pass);

# fonction associées
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("/passerelle/#")

def on_message(client, userdata, msg):
	msg_receipt = str(msg.payload.decode()) 
	print(" message : {} ".format(msg_receipt))
	data_event = json.loads(msg_receipt)	
	send_msg(client_send,data_event);

client = mqtt.Client()
client_send = mqtt.Client()

client.connect("localhost",1883,60)
client_send.connect("192.168.1.3",1883,60)

thread = threading.Thread(target=updateStat, args=(0,))
thread.start()

# callbacks
client.on_connect = on_connect
client.on_message = on_message


client.loop_forever()

