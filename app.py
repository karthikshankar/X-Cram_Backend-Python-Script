from flask import Flask,jsonify,request,json
from datetime import datetime
app = Flask(__name__)
from pymongo import MongoClient
from bson.json_util import dumps

@app.route('/register', methods = ['POST'])
def homepage():
    data = request.data
    dataDict = json.loads(data)
    dataU = dataDict.get("username")
    dataP = dataDict.get("password")
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    client = MongoClient('mongodb://kravuri:xcram@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
    fcram = client['xcram']['users'].find_one({"username":dataU, "password":dataP})
    if(fcram):
        return "Account already exists"
    
    client['xcram']['users'].insert_one(
        {"username":dataDict["username"],
        "password":dataDict["password"],
        "topic":[]}
        )
    doc = client['xcram']['users'].find()
    print([d for d in list(doc)])
    return "You're Registered!"

@app.route('/topic', methods = ['GET'])
def topicReturn():
    data = request.args.get("username")
    dataP = request.args.get("password")
    client = MongoClient('mongodb://kravuri:xcram@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')

    fcram = client['xcram']['users'].find_one({"username":data, "password":dataP})
    if(fcram):
            return dumps(fcram)
    return "Invalid ID"

    
@app.route('/topic/add', methods = ['PUT'])
def changeTopic():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("username")
        dataP = dataDict.get("password")
        client = MongoClient('mongodb://kravuri:xcram@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        fcram = client['xcram']['users'].find_one({"username":data, "password":dataP})


        print(len(fcram["topic"]), fcram["topic"])
        if(len(fcram["topic"]) <  3 and dataDict["topic"] not in fcram["topic"]):
            client['xcram']['users'].update_one(
                {"username":data,
                 "password":dataP},
                {"$push": { "topic": dataDict["topic"] }}
            )
            return dataDict["topic"] + " added"
        else:
            return "too many topics"

@app.route('/topic/delete', methods = ['PUT'])
def deleteTopic():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("username")
        dataP = dataDict.get("password")
        client = MongoClient('mongodb://kravuri:xcram@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        fcram = client['xcram']['users'].find_one({"username":data, "password":dataP})
        client['xcram']['users'].update_one(
                {"username":data,
                 "password":dataP},
                {"$pull": { "topic": dataDict["topic"] }}
            )
        return  dataDict["topic"] + " removed"

    

@app.route('/topic/clear', methods = ['PUT'])
def clearTopic():
        datav = request.data
        dataDict = json.loads(datav)
        data = dataDict.get("username")
        dataP = dataDict.get("password")
        client = MongoClient('mongodb://kravuri:xcram@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        fcram = client['xcram']['users'].find_one({"username":data, "password":dataP})
        client['xcram']['users'].update_one(
                {"username":data,
                 "password":dataP},
                {"$set": { "topic": [] }}
            )
        return "topics cleared"

import re

@app.route('/exercises')
def getExercise():
        client = MongoClient('mongodb://kravuri:xcram@cluster0-shard-00-00-5jiht.mongodb.net:27017,cluster0-shard-00-01-5jiht.mongodb.net:27017,cluster0-shard-00-02-5jiht.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        query = request.args.get('query')
        regex = re.compile(query)
        docs = client['test']['exercises'].find({ "ka_url": regex }, {"_id":0})
        return jsonify(list(docs))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

