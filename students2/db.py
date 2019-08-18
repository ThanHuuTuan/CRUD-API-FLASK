from flask import Blueprint
import pymongo
from pymongo.collection import ObjectId

bp = Blueprint('db', __name__)

_DATABASE_URI="mongodb://localhost:27017"
client = pymongo.MongoClient(_DATABASE_URI)
db = client.students.students

def insert_one(name, lastname, age):
    db.insert_one({"name":name, "lastname":lastname, "age":age})

def find_one(id):
    s = db.find_one({"_id":ObjectId(id)})
    return {'_id':str(s['_id']), 'name':s['name'], 'lastname':s['lastname'], 'age':s['age']}  

def find_id_name(name):
    s = db.find_one({"name":name})
    return str(s['_id'])

def find_all():
    result = []
    for s in db.find():
        result.append({'_id':str(s['_id']), 'name':s['name'], 'lastname':s['lastname'], 'age':s['age']})
    return result

def delete_one(id):
    db.delete_one({"_id":ObjectId(id)})

def update_one(id, name, lastname, age):
    db.update({"_id":ObjectId(id)}, {'name': name, 'lastname':lastname, 'age':age})