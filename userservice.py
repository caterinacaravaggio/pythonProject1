from flask import Flask, request
from markupsafe import escape
from pymongo import MongoClient
import json

app = Flask(__name__)


# mongo --port 27017
# create connection and database

client = MongoClient('mongodb://localhost:27017')
db = client.users

with client:
    #db.userDetails.insert_many(userDetails)
    for x in db.userDetails.find():
        print(x)

#json validation
def validate_json(jsonData):
    print(jsonData)
    try: jsonData['userName']
    except (KeyError, ValueError) as err:
        return err.args[0] + " in json file"
    try: jsonData['name']
    except (KeyError, ValueError) as err:
        return err.args[0] + " in json file"
    try: jsonData['surname']
    except (KeyError, ValueError) as err:
        return err.args[0] + " in json file"
    try: int(jsonData['age'])
    except (KeyError, ValueError) as err:
        return err.args[0] + " in json file"
    if (int(jsonData['age']) <= 0):
        return "incorrect age"
    return "ok"


#create core functions
def insertUser(request):
    code = 1
    #insert in db
    with client:
        #validate request
        ok = validate_json(request.get_json())
        if (ok != "ok"):
            code = -2
            return "Insert not valid:" + ok
        try: db.userDetails.insert(request.get_json())
        except Exception as err:
            code = -2
            ok =  "Failed insert" + err.args[0]
            pass
        #create json string to return
        if code < 0:
            message = '{ "code" : ' + code + ', "defalutMessage" : ' + ok + '}'
        else:
            message = '{ "code" : ' + str(code) + ', "defalutMessage" : "user has been inserted", ' + str(request.get_json()) + ' }'
    return json.dumps(message)
#look at api with json



def getUserDetails(userName):
    code = 0
    #retrive value from db assuming only one value
    with client:
        findUser = list(db.userDetails.find({'userName': userName}, {'_id' : 0}))
        print(findUser)
        if not findUser:
            code = -1
            ok = "Failed find: no matching"
        if code < 0:
            message = '{ "code" : ' + str(code) + ', "defalutMessage" : ' + ok + '}'
        else:
            message = '{ "code" : ' + str(code) + ', "defalutMessage" : "user has been found", ' + str(findUser[0]) + '}'
        jsonResult = json.dumps(message)
    return jsonResult



@app.route('/userService/insertUser', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        return insertUser(request)
    else:
        return 'Error: no %s method' % escape(request.methods)

@app.route('/userService/getUser', methods=['GET', 'POST'])
def find():
    if request.method == 'GET':
        return getUserDetails(request.args.get('userName'))
    else:
        return 'Error %s not method' % escape(request.methods)