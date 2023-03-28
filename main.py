from json import loads
import requests

from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from User import User




@app.route('/testapi')
def testapi():
		return requests.get('http://127.0.0.1:5000/testapi').text


@app.route('/weather/<lat>/<lon>',methods=['GET'])
def weatherby(lat,lon):
	return requests.get('http://127.0.0.1:5000/weather/?lat='+lat+'&lon='+lon).text

@app.route('/forecast/<lat>/<lon>',methods=['GET'])
def weatherforecast(lat,lon):
	return lon


@app.route('/login',methods=['POST'])
def log_in():
	_json = request.json
	_email = _json['email']
	_password = _json['pwd']
	user = mongo.db.user.find_one({'email': _email})

	res:User = loads(dumps(user))
	
	x=check_password_hash(res["pwd"],_password)
	print(x)
	if x:
		return res
	
	return "wrong password"
	



@app.route('/users',methods=['GET'])
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	print(resp)
	return resp

@app.route('/users/add',methods=['POST'])
def add_user():
	print("test1")
	_json = request.json
	_nom = _json['nom']
	_prenom = _json['prenom']
	_email = _json['email']
	_password = _json['pwd']
	if _nom and _prenom and _email and _password and request.method == 'POST':
		_hashed_password = generate_password_hash(_password)
		id = mongo.db.user.insert_one({'nom': _nom,'prenom': _prenom, 'email': _email, 'pwd': _hashed_password})
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		

		
@app.route('/user/<id>',methods=['GET'])
def user(id):
	user = mongo.db.user.find_one({'_id': ObjectId(id)})
	resp = dumps(user)

	return resp

@app.route('/user/update', methods=['PUT'])
def update_user():
	_json = request.json
	_id = _json['_id']
	_nom = _json['nom']
	_prenom = _json['prenom']
	_email = _json['email']
	_password = _json['pwd']		

	if _nom and _prenom and _email and _password and _id and request.method == 'PUT':
		_hashed_password = generate_password_hash(_password)
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'nom': _nom,'prenom': _prenom, 'email': _email, 'pwd': _hashed_password}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp

@app.route('/users/villes', methods=['PUT'])
def add_ville():
	_json = request.json
	_id = _json['_id']
	_ville = _json['ville']
	_pay = _json['pay']
	_lon = _json['lon']
	_lat = _json['lat']


	if _ville and _pay and _lon and _lat and _id and request.method == 'PUT':
		ville={'ville': _ville,'pay': _pay, 'lon': _lon, 'lat': _lat}
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$push':{ "villes": ville } })
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()

@app.route('/user/ville/delete/<id>/<ville>', methods=['DELETE'])
def delete_ville(id,ville):
	_id = id
	villeobj={'ville': "xxxx",'pay': "xxx", 'lon': 123, 'lat': 123}
	print("ville:",ville)
	mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$pull':{ "villes": {"ville": ville} } })


	resp = jsonify('Ville deleted successfully!')
	resp.status_code = 200
	return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
	
    app.run(port=5002)
