from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Cannot be left blank.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item does not exist."}, 404

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Item {} already exists !!!".format(name)}, 400
        data = Item.parser.parse_args()
        newItem = ItemModel(name, data['price'])
        try:
            newItem.save_to_db()
        except:
            return {"message": "Error occurred while inserting new item"}, 500

        return newItem.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {"message": "Error occurred while updating item"}, 500

        return item.json()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        #items = []
        # for r in ItemModel.get_all():
        #    items.append({"name": r[1], "price": r[2]})
        # return {'items': items if items else None}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
