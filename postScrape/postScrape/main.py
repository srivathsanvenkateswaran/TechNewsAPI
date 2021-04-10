from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/user.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    key = db.Column(db.String(), unique=True, nullable=False)

    def repr(self):
        return f'username: {self.username}, key: {self.key}'

def generateAPI_KEY():
    import secrets
    key = secrets.token_urlsafe(16)
    return key

def getJsonFromFile(filename):
    import json
    with open(f"results/{filename}" , 'r') as f:
        return json.loads(f.read())

def validateAPI_KEY(uname, API_KEY):
    temp = User.query.filter_by(username=uname).all()
    if len(temp)<=0:
        abort(404, message="User doesn't exist")
    else:
        return temp[0].key == API_KEY

class Article(Resource):
    def get(self, uname, CodeString):
        if(validateAPI_KEY(uname, CodeString)):
            return {
                "status" : 'OK', 
                "response" : getJsonFromFile("finalArticleList.json") 
            }
        else:
            return{
                "status" : 'NOT OK',
                "error" : 'Invalid API_KEY'
            }
    
    def put(self, uname, CodeString):
        if(CodeString == "shivajiVaailaJilebi"):
            temp = User.query.filter_by(username=uname).all()
            if len(temp)>0:
                return f"User {temp[0].username} already exists with API_KEY: {temp[0].key}", 201
            else:
                user = User()
                user.username = uname
                user.key = generateAPI_KEY()
                db.session.add(user)
                db.session.commit()
                return f"New user {user.username} with API_KEY: {user.key} created", 201
        else:
            return "You are unauthorized", 401


api.add_resource(Article, "/getNews/<string:uname>/<string:CodeString>")    

if __name__ == "__main__":
    app.run(debug=True)
