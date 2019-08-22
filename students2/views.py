from flask import (Blueprint, request, jsonify, Response)
from bson.errors import InvalidId

from students2 import db 
from students2.cache import (get_one, get_all, try_connection)
bp = Blueprint('views', __name__)

@bp.route('/students', methods=['GET','POST'])
def get_post():
    '''
    1.Lets you get all the student with a GET request.
    2.Lets you add a new student with a POST request by suplying the 
      users name lastname ang age in JSON format.
    '''
    if request.method == 'GET':
        if try_connection():
            res = get_all()
        else:
            res = []
        if len(res) == 0:
            res = db.find_all()
            if len(res) == 0:
                return {'result': 'No users'}
        return jsonify(res) 
    elif request.method == 'POST':
        try:
            name = request.json['name']
            lastname = request.json['lastname']
            age = request.json['age']
        except (TypeError, KeyError):
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Missing field"}')
        db.insert_one(name, lastname, age)
        return {'message': 'Added User'}

@bp.route('/students/<string:id>', methods=['GET', 'PATCH', 'DELETE'])
def update_delete_get(id):
    '''
    1.Lets you get one student with a GET request by suplying the student ID .
    2.Lets you delete a student with a DELETE request by suplying the student ID.
    2.Lets you delete a student with a PATCH request by suplying the student ID 
      and the users name lastname ang age in JSON format.
    '''
    if request.method == 'GET':
        if try_connection():
            try:
                res = get_one(id)
            except (TypeError, InvalidId):
                try:    
                    res = db.find_one(id)
                except (InvalidId, TypeError):
                    return Response(status=400, mimetype='application/json',
                                response='{"result": "Doesn\'t exist in DB!!"}')
            return jsonify(res)
        else:
            try:    
                res = db.find_one(id)
            except (InvalidId, TypeError):
                return Response(status=400, mimetype='application/json',
                            response='{"result": "Doesn\'t exist in DB!!"}')
        return jsonify(res)
    elif request.method == 'DELETE':
        try:
            res = db.delete_one(id)
        except InvalidId:
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Doesn\'t exist in DB!!"}')
        return {'message': 'Deleted User'}
    elif request.method == 'PATCH':
        try:
            name = request.json['name']
            lastname = request.json['lastname']
            age = request.json['age']
        except (TypeError, KeyError):
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Missing field"}')
        try:
            db.update_one(id, name, lastname, age)
        except InvalidId:
            return Response(status=400, mimetype='application/json', 
                            response='{"result": "Invalid Id!!"}')
        return {'message': 'Patched User'}
