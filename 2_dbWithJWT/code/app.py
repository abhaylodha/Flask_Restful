from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
import datetime
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "ak"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=18000)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/adduser")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
