from flask import Flask
from pymongo import MongoClient
import json
app = Flask(__name__)

#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017,username='adm-mongo',password='mongo707-2022',authSource='admin')
db=client.db_evenement
collection = db.db_evenement

@app.route('/accident')
def get_accident():
    cursor = collection.find()
    list_cur = list(cursor)
    print(list_cur)
    for l in list_cur:
      l.pop("_id")
      l["id"] = int(l.pop("id"))
      l["date_debut"] = l.pop("dateDebutEvenement")
      l["date_fin"] = l.pop("dateFinEvenement")
      l["nb_pers"] = int(l.pop("nombreVehicules"))
      l["position"] = l.pop("positions")
    json_data=json.dumps(list_cur)
    print(json_data)
    return json_data

if __name__ == "__main__":
    app.run(host="192.168.1.6")

