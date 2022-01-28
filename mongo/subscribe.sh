#!/usr/bin/python3
import pika
from pymongo import MongoClient
import json
import time
from datetime import datetime

#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017,username='adm-mongo',password='mongo707-2022',authSource='admin')
db=client.db_evenement
collection = db.db_evenement

def addDatabase(msg):
    print(msg)
    data = json.loads(msg)
    if data['etat'] == "en cours":
       data['libelle_evenement'] = data.pop('evenement')
       data['positions'] = data.pop('position')
       data['nombreVehicules'] = 1
       data['id'] = data.pop('id_evenement')
       dt_obj =  datetime.fromtimestamp(data['timestamp'])
       data['dateDebutEvenement'] = dt_obj.strftime("%d/%m/%Y %Hh%M")
       data['dateFinEvenement'] = ""
       data.pop('timestamp')
       data.pop('id_vehicule')
       data.pop('type_msg')
    elif data['etat'] == "fin":
       dt_obj =  datetime.fromtimestamp(data['timestamp'])
       data['dateFinEvenement'] = dt_obj.strftime("%d/%m/%Y %Hh%M")
    print(data)
    try:
       if data['etat'] == "en cours":
          data.pop('etat')
          print("coucou")
          collection.insert_one(data)
       else:
          collection.update_one({"id": data['id_evenement']}, { "$set": {"dateFinEvenement": data['dateFinEvenement']} })
    except:
       print("error")

def callback(ch, method, properties, body):
	addDatabase(body.decode())
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.4'))

channel = connection.channel()

channel.queue_declare(queue='accident')

print(" En attente de message ")

channel.basic_consume('accident',callback,auto_ack=True)

channel.start_consuming()

