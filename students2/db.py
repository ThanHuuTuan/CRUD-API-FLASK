from flask import Blueprint
from pymongo.collection import ObjectId
import pymongo
from students2 import cache

bp = Blueprint('db', __name__)

_DATABASE_URI='mongodb://localhost:27017'
client = pymongo.MongoClient(_DATABASE_URI)
db = client.students.students


def insert_one(name, lastname, age):
    db.insert_one({'name':name, 'lastname':lastname, 'age':age})
    if cache.try_connection():
        id = find_id_name(name)
        cache.set_one(id, name, lastname, age)

def find_id_name(name):
    s = db.find_one({'name':name})
    return str(s['_id'])

def find_one(id):
    s = db.find_one({'_id':ObjectId(id)})
    if cache.try_connection():
        #add the student to cache too
        cache.set_one(str(s['_id']),s['name'],s['lastname'],s['age'])
    return {'_id':str(s['_id']), 'name':s['name'], 'lastname':s['lastname'], 'age':s['age']}  

def find_all():
    result = []
    for s in db.find():
        #adds them all to cache too
        result.append({'_id':str(s['_id']), 'name':s['name'], 'lastname':s['lastname'], 'age':s['age']})
        if cache.try_connection():
            cache.set_one(str(s['_id']),s['name'],s['lastname'],s['age'])
    return result

def delete_one(id):
    db.delete_one({'_id':ObjectId(id)})
    if cache.try_connection():
        #also deletes from cache
        cache.delete_one(id)

def update_one(id, name, lastname, age):
    db.update({'_id':ObjectId(id)}, {'name': name, 'lastname':lastname, 'age':age})
    if cache.try_connection():
        cache.delete_one(id)
        cache.set_one(str(id), name, lastname, age)
