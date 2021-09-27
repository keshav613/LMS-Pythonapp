# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, request
from bson.json_util import dumps
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)
# connecting with DB
uri = "mongodb+srv://"+uname+":"+pwd+"@keshav-lms.biuic.mongodb.net/"+dbName+"?retryWrites=true&w=majority"
mongodb_client = PyMongo(app, uri)
db = mongodb_client.db

#Api Routing
@app.route('/LMS/', methods = ['GET'])
def home():
	if(request.method == 'GET'):
		return ("Welcome to Keshav's Library Management System. Use CRUD operations with REST Api" ,202)


@app.route('/LMS/addBook', methods = ['POST'])
def addBook():
	body = request.json
	author, bookName = body["author"], body["bookName"]
	if(request.method == 'POST'):	
		db.books.insert_one({'author':author , 'bookName': bookName})
		return ("Success, book added !!", 200)
	else:
		return not_found()

@app.route('/LMS/updateBook', methods=['PUT'])
def updateBook():
	body = request.json
	id ,author, bookName = body['id'],body["author"], body["bookName"]
	if(request.method == 'PUT' and id):
		db.books.replace_one({'_id':ObjectId(id)}, {'author':author, 'bookName':bookName})
		return ("Success, book edited !!", 200)
	else:
		return not_found()

@app.route('/LMS/getBooks/', methods=['GET'])
def getBooks():
	args = request.args
	id, author, bookName = args.get("id"), args.get("author"),args.get("bookName")
	print(id,author,bookName)
	if(id):
		return (dumps(db.books.find_one({'_id': ObjectId(id)}),default=json_util.default), 200)
	elif(author):
		return (dumps(db.books.find_one({'author': author}), default=json_util.default),200)
	elif(bookName):
		return (dumps(db.books.find_one({'bookName': bookName}), default=json_util.default),200)

	else:
		return (dumps(db.books.find(), default=json_util.default),200)

@app.route("/LMS/deleteBook",methods=['DELETE'])
def deleteBook():
	id = request.json['id']
	if( db.books.find_one({'_id': ObjectId(id)}) ):
		db.book.delete_one({'_id': ObjectId(id)})
		return ("Book deleted!!",200)
	else:
		return ("Invalid ID",404)

@app.errorhandler(404)
def not_found(error=None):
	return ({
		"status" : 404,
		"message" : "Page Not Found " + request.url
	},404)

# driver function
if __name__ == '__main__':
	app.run(host="0.0.0.0",debug = True,port=80)
