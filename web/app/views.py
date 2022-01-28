import json
import requests
from flask import Flask
from flask import render_template


app = Flask(__name__)

accidents = None

@app.route('/')
def index():
    data_acc = None
    data_stat = None
    with open("/json-save/accident.json", "r") as read_file:
    	data_acc = json.load(read_file)
    with open("/json-save/stat.json", "r") as read_file:
        data_stat = json.load(read_file) 
    print(data_stat)
    return render_template("index.html",accidents=data_acc["accidents"], stat=data_stat)

@app.route('/historique')
def history():
   r = requests.get('http://192.168.1.6:5000/accident')
   data = r.json()
   return render_template("history.html",accidents=data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

