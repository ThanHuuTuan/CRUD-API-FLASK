from flask import Blueprint
from json import (loads, dumps)
import redis

bp = Blueprint('cache', __name__)
client = redis.StrictRedis()
_path='.'

def try_connection():
    try:
        client.ping()
    except redis.ConnectionError:
        return False
    return True

def set_data(mkey, mval):
    client.execute_command('JSON.SET', 's'+mkey, _path, dumps(mval))
        
def get_one(mkey):
    return loads(client.execute_command('JSON.GET', 's'+str(mkey)))

def set_one(id, name, lastname, age):
    mkey = str(id)
    mval = {'_id':id, 'name':name, 'lastname':lastname, 'age':age}
    set_data(mkey, mval)

def delete_one(mkey):
    client.execute_command('JSON.DEL', 's'+str(mkey))

def get_all():
    result = []
    for k in client.keys('s*'):
        val = loads(client.execute_command('JSON.GET', k))
        result.append(val)
    return result