from flask import Blueprint
from pymongo.collection import ObjectId
import pymongo
from students2 import chace

bp = Blueprint('db', __name__)

_DATABASE_URI="mongodb://localhost:27017"
client = pymongo.MongoClient(_DATABASE_URI)
db = client.students.students

def insert_one(name, lastname, age):
    db.insert_one({"name":name, "lastname":lastname, "age":age})
    id = find_id_name(name)
    chace.set_one(id, name, lastname, age)

def find_id_name(name):
    s = db.find_one({"name":name})
    return str(s['_id'])

def find_one(id):
    s = db.find_one({"_id":ObjectId(id)})
    #add the student to chace too
    chace.set_one(str(s['_id']),s['name'],s['lastname'],s['age'])
    return {'_id':str(s['_id']), 'name':s['name'], 'lastname':s['lastname'], 'age':s['age']}  

def find_all():
    result = []
    for s in db.find():
        #adds them all to chace too
        result.append({'_id':str(s['_id']), 'name':s['name'], 'lastname':s['lastname'], 'age':s['age']})
        chace.set_one(str(s['_id']),s['name'],s['lastname'],s['age'])
    return result

def delete_one(id):
    db.delete_one({"_id":ObjectId(id)})
    #also deletes from chace
    chace.delete_one(id)

def update_one(id, name, lastname, age):
    db.update({"_id":ObjectId(id)}, {'name': name, 'lastname':lastname, 'age':age})
    chace.delete_one(id)
    chace.set_one(str(id), name, lastname, age)