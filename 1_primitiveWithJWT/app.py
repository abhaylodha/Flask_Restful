from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import datetime

app = Flask(__name__)
app.secret_key = "ak"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=18000)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Cannot be left blank.")

    # @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    # @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": "Item {} already exists !!!".format(name)}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        return {"item": item}


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {'items': items if items else None}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)
