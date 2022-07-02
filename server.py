from flask import Flask, render_template, request,redirect,url_for
import pymongo
from datetime import datetime
import string
import random
import json
import os
import socket
app = Flask(__name__)
data = {}

def random_url_generator():
    letters = string.ascii_lowercase
    link=''.join(random.choice(letters) for i in range(10)) 
    return link
try:
        with open("config.json", "r") as config:
            data = json.load(config)
            print(data)
except:
    print("Could not fetch config! Loading from default configs...")
    data['minutes_to_expire']= 5
    data['port'] = 8000
    data['hostname'] = "mongo-svc"

username = os.getenv('PYMONGO_USERNAME')
password = os.getenv('PYMONGO_PASSWORD')

if username is None or password is None:
        print("Entered default secret")
        username = "rohamzn"
        password = "75321475"

client = pymongo.MongoClient(host=data['hostname'],port=27017,username=username,password=password,authSource="admin")

db = client['data']
notes= db['notes']

@app.route("/")
def index():
    return render_template("submit_note.html")


@app.route("/insertNote",methods=["POST"])
def insertNote():
    note= request.form['note'] 
    url = random_url_generator()
    notes.insert_one({"id":url,"time":datetime.today(),"note":note,"available":True})
    return render_template("url.html",note="127.0.0.1:5000/warningPage/"+url,url=url)
    
@app.route("/warningPage/<id>",methods=["GET"])
def warningPage(id):

    note = notes.find_one({"id":id})
    if(note['available']) == True:
        spend = (datetime.now() - note['time']).total_seconds()
        if (spend > data['minutes_to_expire'] * 60):
            notes.update_one({"id":id},{ "$set": { 'available': False } })
            return "not available"
        return render_template("warning.html", id = id)
    else:
        return "note not available"
@app.route("/showNotePage",methods=["POST"])
def showNotePage():
    id = request.form['btn']
    notes.update_one({"id":id},{ "$set": { 'available': False } })
    print("id", id)
    return render_template("note.html", text = notes.find_one({"id":id})['note'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
