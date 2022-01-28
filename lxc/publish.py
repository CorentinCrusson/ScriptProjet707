  GNU nano 6.0                                                                                                    publish.py                                                                                                               
#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import random

vitesse = 90+random.randrange(20)
time_veh = 93+random.randrange(50)
id_veh = int(time.time())-(1643218410+random.randrange(10))
accident_time = round(random.uniform(70, time_veh-20), 1)

print(accident_time)
print(accident_time-30)

# publish(file,msg)
def envoiMessage(msg):
    print("ping id"+str(id_veh))
    client.publish("/passerelle/"+str(id_veh), msg);


# connect (addr,port,keepalive)
client = mqtt.Client()
client.connect("192.168.1.7",1883,60)

while time_veh > 0:
    position_Lo = random.uniform(47.4210, 49.6152)
    position_La = random.uniform(41.4897, 48.2310)
    envoiMessage("{\"type_msg\": \"CAM\", \"vitesse\":"+str(vitesse)+",\"id_vehicule\":"+str(id_veh)+", \"position_gps\": \""+str(position_Lo)+", "+str(position_La)+"\"}")
    if round(time_veh,1) == 60.1:
       vitesse = 0
       time_veh - 0.1
       id_acc = int(time.time())-1643218458
       envoiMessage("{\"type_msg\": \"DENM\", \"evenement\": \"accident\", \"id_evenement\": "+str(id_acc)+", \"id_vehicule\": "+str(id_veh)+", \"position\": \""+str(position_Lo)+", "+str(position_La)+"\", \"timestamp\": "+str(int(tim>
    elif round(time_veh,1) == 50.1:
       vitesse = 90
       time_veh - 0.1
       envoiMessage("{\"type_msg\": \"DENM\", \"evenement\": \"accident\",\"id_evenement\": "+str(id_acc)+", \"id_vehicule\": "+str(id_veh)+", \"position\": \""+str(position_Lo)+", "+str(position_La)+"\", \"timestamp\": "+str(int(time>

    if vitesse >= 90:
       time_veh = time_veh - 0.1
       time.sleep(0.1)
    else:
       time_veh = time_veh - 1
       time.sleep(1)
    print(time_veh)

client.disconnect();

