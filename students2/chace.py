from flask import Blueprint
from flask.cli import with_appcontext
import click

import redis 
from json import (loads, dumps)
from students2.db import (find_all, find_one, delete_one, insert_one, update_one)

bp = Blueprint('chace', __name__)

client = redis.StrictRedis()
_path='.'

def set_data(mkey, mval):
    client.execute_command('JSON.SET', 's'+mkey, _path, dumps(mval))

def get_one(mkey):
    return loads(client.execute_command('JSON.GET', 's'+str(mkey)))

def set_one(id, name, lastname, age):
    mkey = str(id)
    mval = {"_id":id, "name":name, "lastname":lastname, "age":age}
    set_data(mkey, mval)

def delete_one(mkey):
    client.execute_command('JSON.DEL', 's'+str(mkey))

def get_all():
    result = []
    for k in client.keys('s*'):
        val = loads(client.execute_command('JSON.GET', k))
        result.append(val)
    return result

def set_all():
    students = find_all()
    for s in students:
        mkey = set_one(s['_id'], s['name'], s['lastname'], s['age'])

@click.command('init-chace')
@with_appcontext
def init_chace_command():
    '''Command that initializes the chace with all the db users.'''
    set_all()
    click.echo('[*] Initialized Chace - OK')

def init_chace(app):
    app.cli.add_command(init_chace_command)
