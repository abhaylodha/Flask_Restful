from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
import datetime
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db

app = Flask(__name__)
# It turns off Flask SQLAlchemy tracker as it consumes more resources.
# Underlying SQLAlchemy has a very good tracker. So no issues in turning it off.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.secret_key = "ak"
api = Api(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=18000)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/adduser")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
