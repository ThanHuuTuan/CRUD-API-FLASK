from flask import (Blueprint, request, jsonify, Response)
from bson.errors import InvalidId
from students2 import db 
from students2.cache import (get_one, get_all, try_connection)

bp = Blueprint('views', __name__)

@bp.route('/students', methods=['GET'])
def get_students():
	if request.method == 'GET':
		if try_connection():
			res = get_all()
		else:
			res = []
		if len(res) <= db.db.count_documents(filter={}):
			res = db.find_all()
			if len(res) == 0:
				return {'result': 'No users'}
		return jsonify(res) 

@bp.route('/students', methods=['POST'])
def add_student(): 
	if request.method == 'POST':
		try:
			name = request.json['name']
			lastname = request.json['lastname']
			age = request.json['age']
		except (TypeError, KeyError):
			return Response(status=400, mimetype='application/json', 
							response='{"result": "Missing field"}')
		db.insert_one(name, lastname, age)
		return Response(status=201, mimetype='application/json',
						response='{"message": "Added User"}')

@bp.route('/students/<string:id>', methods=['GET'])
def get_student(id):
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

@bp.route('/students/<string:id>', methods=['DELETE'])
def delete_student(id):
	if request.method == 'DELETE':
		try:
			res = db.delete_one(id)
		except InvalidId:
			return Response(status=400, mimetype='application/json', 
							response='{"result": "Doesn\'t exist in DB!!"}')
		return {'message': 'Deleted User'}

@bp.route('/students/<string:id>', methods=['PATCH'])
def patch_student(id):
	if request.method == 'PATCH':
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
