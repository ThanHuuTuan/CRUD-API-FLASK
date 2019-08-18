from flask import (Blueprint, request, jsonify, Response)
from bson.errors import InvalidId

from students2 import db #(db.find_all, db.find_one, db.delete_one, db.insert_one, db.update_one)
from students2 import chace # (set_one, get_one, get_all, set_all, delete_one  )
bp = Blueprint('views', __name__)



@bp.route('/students', methods=['GET','POST'])
def get_post():
    '''
    1.Lets you get all the student with a GET request.
    2.Lets you add a new student with a POST request by suplying the 
      users name lastname ang age in JSON format.
    '''
    if request.method == 'GET':
        res = chace.get_all()
        if len(res) == 0:
            return {'result': 'No users'}
        else:
            return jsonify(res) 
    elif request.method == 'POST':
        try:
            name = request.json['name']
            lastname = request.json['lastname']
            age = request.json['age']
        except KeyError:
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Missing field"}')
        db.insert_one(name, lastname, age)
        id = db.find_id_name(name)
        chace.set_one(id, name, lastname, age)
        return {'message': 'Added User'}

@bp.route('/students/<string:id>', methods=['GET', 'PATCH', 'DELETE'])
def update_delete_get(id):
    '''
    1.Lets you get one student with a GET request by suplying the student ID .
    2.Lets you delete a student with a DELETE request by suplying the student ID.
    2.Lets you delete a student with a DELETE request by suplying the student ID 
      and the users name lastname ang age in JSON format.
    '''
    if request.method == 'GET':
        try:
            res = chace.get_one(id)
        except TypeError:
            try:    
                res = db.find_one(id)
            except InvalidId:
                return Response(status=400, mimetype='application/json',
                            response='{"result": "Doesn\'t exist in DB!!"}')
        return jsonify(res)
    elif request.method == 'DELETE':
        try:
            res = db.delete_one(id)
            chace.delete_one(id)
        except InvalidId:
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Doesn\'t exist in DB!!"}')
        return {'message': 'Deleted User'}
    elif request.method == 'PATCH':
        try:
            name = request.json['name']
            lastname = request.json['lastname']
            age = request.json['age']
        except KeyError:
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Missing field"}')
        try:
            db.update_one(id, name, lastname, age)
        except InvalidId:
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Invalid Id!!"}')
            chace.delete_one(id)
            chace.set_one(id, name, lastname, age)
        return {'message': 'Patched User'}
