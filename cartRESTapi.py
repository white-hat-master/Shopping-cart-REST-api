from flask import Flask, request, Response, json, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Creating MongoDB interactor
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["shoppingCartRESTapi"]

# route start here
@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')
# Get users
@app.route('/users', methods=['GET'])
def getUsers():
    users = mydb["users"]
    output = []
    for i in users.find():
        output.append({'name': i['name'], 'email': i['email']})
    return Response(response=json.dumps({'All Users': output}),
                    status=200,
                    mimetype='application/json')

# Read all items
@app.route('/items', methods=['GET'])
def getItems():
    items = mydb["items"]
    output = []
    for i in items.find():
        output.append({'name': i['name'], 'price': i['price']})
    return Response(response=json.dumps({'All Items': output}),
                    status=200,
                    mimetype='application/json')

# Create item
@app.route('/addItem', methods=['POST'])
def addItem():
    items = mydb["items"]
    data = request.json
    # print(data)
    if data is None or data == {} or 'name' not in data or 'price' not in data:
        return Response(response=json.dumps({"Error": "Please provide information"}),
                        status=400,
                        mimetype='application/json')
    response = items.insert_one(data)
    return Response(response=json.dumps({'result': "Item added Successfully", 'Document_ID': str(response.inserted_id)}),
                    status=200,
                    mimetype='application/json')

# Update Item
@app.route('/updateItem', methods=['PUT'])
def updateItem():
    items = mydb["items"]
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide information"}),
                        status=400,
                        mimetype='application/json')
    myQuery = {"name": data["name"]}
    myData = {"$set": data}
    response = items.update(myQuery, myData)

    return Response(response=json.dumps({'result': "Item Updated Successfully"}),
                    status=200,
                    mimetype='application/json')
# delete item
@app.route('/deleteItem', methods=['DELETE'])
def deleteItem():
    items = mydb["items"]
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide information"}),
                        status=400,
                        mimetype='application/json')
    myQuery = {"name": data["name"]}
    response = items.delete_one(myQuery)

    return Response(response=json.dumps({'result': "Item Deleted Successfully"}),
                    status=200,
                    mimetype='application/json')
# Read all Carts
@app.route('/carts', methods=['GET'])
def getCarts():
    carts = mydb["carts"]
    output = []
    for i in carts.find():
        output.append({
            'name': i['name'],
            'email': i['email'],
            'items': i['allItems']    
        })
    
    return Response(response=json.dumps({'All Carts': output}),
                    status=200,
                    mimetype='application/json')

# Create Cart
@app.route('/createCart', methods=['POST'])
def createCart():
    carts = mydb["carts"]
    data = request.json
    # print(data)
    if data is None or data == {} or 'name' not in data or 'email' not in data or 'items' not in data:
        return Response(response=json.dumps({"Error": "Please provide information"}),
                        status=400,
                        mimetype='application/json')
        
    newUserData = {
        'name' : data['name'],
        'email' : data['email']
    }
    newUser = mydb['users'].insert_one(newUserData)
    
    if newUser.inserted_id:
        cartData = {
            'name' : data['name'],
            'email' : data['email'],
            'allItems' : data['items']
        }
        response = carts.insert_one(cartData)
        return Response(response=json.dumps({'result': "Cart Created and Items added Successfully", 'Document_ID': str(response.inserted_id)}),
                        status=200,
                        mimetype='application/json')

# Update Cart
@app.route('/updateCart', methods=['PUT'])
def updateCart():
    carts = mydb["carts"]
    data = request.json
    # print(data)
    if data is None or data == {} or 'name' not in data or 'email' not in data or 'items' not in data:
        return Response(response=json.dumps({"Error": "Please provide information"}),
                        status=400,
                        mimetype='application/json')
    myQuery = { 'email' : data['email'] }
    if carts.find_one(myQuery):
        cartData = {
            'name' : data['name'],
            'email' : data['email'],
            'allItems' : data['items']
        }
        response = carts.update_one(myQuery,{'$set':cartData})
        return Response(response=json.dumps({'result': "Items added Successfully"}),
                        status=200,
                        mimetype='application/json')
    return Response(response=json.dumps({'result': "Please Right Provide Information."}),
                        status=200,
                        mimetype='application/json')    
       
# Delete Cart
@app.route('/deleteCart', methods=['DELETE'])
def deleteCart():
    carts = mydb["carts"]
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide information"}),
                        status=400,
                        mimetype='application/json')
    myQuery = {"email": data["email"]}
    response = carts.delete_one(myQuery)

    return Response(response=json.dumps({'result': "Item Deleted Successfully"}),
                    status=200,
                    mimetype='application/json')
# Creating a Flask Server
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
