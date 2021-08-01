# Using flask to make an api
# import necessary libraries and functions
from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
app = Flask(__name__)
# connecting with DB
uname,pwd,dbName = "keshav","forgotpassword","lms"
uri = "mongodb+srv://"+uname+":"+pwd+"@keshav-lms.biuic.mongodb.net/"+dbName+"?retryWrites=true&w=majority"
mongodb_client = PyMongo(app, uri)
db = mongodb_client.db

#Api Routing
@app.route('/LMS/', methods = ['GET'])
def home():
	if(request.method == 'GET'):
		return ("Welcome to Keshav's Library Management System. Use CRUD operations with REST Api" ,202)


@app.route('/LMS/addBooks', methods = ['POST'])
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
		book = db.books.find_one({'_id': ObjectId(id)})
		return (jsonify(book), 200)
	elif(author):
		book = db.books.find_one({'author': author})
		return (jsonify(book), 200)
	elif(bookName):
		book = db.books.find_one({'bookName': bookName})
		return (jsonify(book), 200)
	else:
		books = db.books.find()
		return (jsonify(books), 200)

@app.route("/LMS/deleteBook",methods=['DELETE'])
def deleteBook():
	id = request.json['id']
	db.book.delete_one({'_id':ObjectId(id)})
	return ("Book deleted!!",200)

@app.errorhandler(404)
def not_found(error=None):
	return ({
		"status" : 404,
		"message" : "Page Not Found " + request.url
	},404)

# driver function
if __name__ == '__main__':
	app.run(debug = True,port=80)
