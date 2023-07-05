from flask import Flask, request
import requests
import pymysql
from app import app
from db_config import mysql
from flask import jsonify

@app.route('/userss/<id>', methods=['GET'])
def get_user(id):
    url = f'http://httpbin.org/get?id={id}'
    response = requests.get(url)
    return response.json()

@app.route('/userss', methods=['POST'])
def addd_user():
    data = request.get_json()
    url = 'http://httpbin.org/post'
    response = requests.post(url, json=data)
    return response.json()

# To get users details of specific id 
@app.route('/user/<int:id>')
def user(id):
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE id=%s", id)
        row = cursor.fetchone()
        if row:
            resp = jsonify(row)
            resp.status_code = 200
            return resp
        resp = jsonify({"error":"User not found"})
        resp.status_code = 404
        return resp 
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

# To create users and save to db - POST api
@app.route('/user', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		# validate the received values
		if _name and _email and request.method == 'POST':
            #saving values into db
			sql = "INSERT INTO user(name,email) VALUES(%s, %s)"
			data = (_name, _email)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify({"success":True, "message":"User created successfully"})
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
  
# To handle url errors
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

# Main function of the file
if __name__ == "__main__":
    app.run()