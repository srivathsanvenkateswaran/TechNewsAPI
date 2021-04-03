from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

# TO DO
# 
# Host the spider and this API in any hosting provider

API_KEY_DICTIONARY = {}

def generateAPI_KEY(username):
    import secrets
    key = secrets.token_urlsafe(16)
    API_KEY_DICTIONARY[username] = key
    return key

def getJsonFromFile(filename):
    import json
    with open(f"results/{filename}" , 'r') as f:
        return json.loads(f.read())

def validateAPI_KEY(username, API_KEY):
    if username not in API_KEY_DICTIONARY:
        abort(404, message="User doesn't exist")

    if username in API_KEY_DICTIONARY:
        return API_KEY_DICTIONARY[username] == API_KEY
    else:
        return False

class Article(Resource):
    def get(self, username, API_KEY):
        if(validateAPI_KEY(username, API_KEY)):
            return {
                "status" : 'OK', 
                "response" : getJsonFromFile("finalArticleList.json") 
            }
        else:
            return{
                "status" : 'NOT OK',
                "error" : 'Invalid API_KEY'
            }
    
    def put(self, username, API_KEY):
        if username in API_KEY_DICTIONARY:
            return f"User {username} already exists with API_KEY: {API_KEY_DICTIONARY[username]}", 201
        else:
            API_KEY_DICTIONARY[username] = generateAPI_KEY(username)
            return f"New user {username} with API_KEY: {API_KEY_DICTIONARY[username]} created", 201


api.add_resource(Article, "/getNews/<string:username>/<string:API_KEY>")    

if __name__ == "__main__":
    app.run(debug=True)

# srivathsan k1xZcgl3_L6Cza1hM217Vg