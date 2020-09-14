from flask import Flask, request,  jsonify
from markupsafe import escape
from pymongo import MongoClient
import logging
import yaml

app = Flask(__name__)

with open("app.conf.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)

logging.basicConfig(filename=config['logger']['filename'], level=config['logger']['level'])

logging.info("Program started")
# mongo --port 27017
# create connection and database

client = MongoClient('mongodb://' + config['database']['mongodb']['host'] + ':' + config['database']['mongodb']['port'])
db = client.config['database']['mongodb']['db']
logging.info("Connected to DB")

with client:
    logging.info("Current UserDetails \n" + '\n'.join(str(elem) for elem in list(db.userDetails.find())))


# json validation
def validate_json(jsonData):
    result = "user has been saved"
    try:
        username = jsonData['userName']
    except (KeyError, ValueError) as err:
        logging.error(err.args[0] + " in json file")
        result = err.args[0] + " in json file"
        username = 'error'
        pass
    try:
        name = jsonData['name']
    except (KeyError, ValueError) as err:
        logging.error(err.args[0] + " in json file")
        result = err.args[0] + " in json file"
        name = 'error'
        pass
    try:
        surname = jsonData['surname']
    except (KeyError, ValueError) as err:
        logging.error(err.args[0] + " in json file")
        result = err.args[0] + " in json file"
        surname = 'error'
        pass
    try:
        age = int(jsonData['age'])
    except (KeyError, ValueError) as err:
        logging.error(err.args[0] + " in json file")
        result = err.args[0] + " in json file"
        age = 1
        pass

    if (age <= 0):
        logging.error("incorrect age")
        result = "incorrect age"
        pass


    if not username:
        result = "void field username"

    if not name:
        result = "void field name"

    if not surname:
        result = "void field surname"


    logging.info("Row ready to be inserted")

    return result


# create core functions
def insertUser(request):
    logging.info("Request for insert user")
    code1 = 1
    # insert in db
    with client:
        # validate request
        ok = validate_json(request)
        if (ok != "user has been saved"):
            code1 = -2
            logging.error("Not valid insert: " + ok)
        logging.info("Starting insert")
        try:
            db.userDetails.insert(request)
        except Exception as err:
            logging.error("Failed insert" + err.args[0])
            code1 = -2
            ok = "Failed insert" + err.args[0]
            pass
        # create json string to return
        if code1 < 0:
            message = jsonify(code=code1, defaultMessage=ok)
        else:
            message = jsonify(code=code1, defaultMessage=ok , userName=request['userName'],
                              name=request['name'], surname=request['surname'], age=request['age'])

    return message


# look at api with json


def getUserDetails(userName):
    logging.info("Request for find user")
    code1 = 1
    # retrive value from db assuming only one value
    if not userName:
        ok = "Error : Invalid request"
        code = -1
    else:
        with client:
            findUser = list(db.userDetails.find({'userName': userName}, {'_id': 0}))
            # print(findUser)
            if not findUser:
                logging.error("Failed find: no matching")
                code1 = -1
                ok = "Failed find: no matching"
            else:
                logging.info("Row present in DB")
                ok = "user has been found"
    if code1 < 0:
        message = jsonify(code=code1, defaultMessage=ok)
    else:
        message = jsonify(code=code1, defaultMessage=ok , users=findUser)

    return message


@app.route(config['routes']['insert']['url'], methods=['GET', 'POST'])
def insert():
    logging.info("Insert request")
    if request.method == 'POST':
        return insertUser(request.get_json())
    else:
        logging.error("GET request ")
        return 'Error: no %s method' % escape(request.methods)


@app.route(config['routes']['get']['url'], methods=['GET', 'POST'])
def find():
    logging.info("Find Request")
    if request.method == 'GET':
        return getUserDetails(request.args.get('userName'))
    else:
        logging.error("POST request ")
        return 'Error %s not method' % escape(request.methods)


if __name__ == '__main__':
    app.run(port=9000)
