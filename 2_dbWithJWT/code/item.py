import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Cannot be left blank.")

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message": "Item does not exist."}, 404

    # @jwt_required()
    def post(self, name):
        if Item.find_by_name(name):
            return {"message": "Item {} already exists !!!".format(name)}, 400
        data = Item.parser.parse_args()
        try:
            Item.insert_new(name, data['price'])
        except:
            return {"message": "Error occurred while inserting new item"}, 500

        return {"name": name, "price": data['price']}, 201

    def delete(self, name):
        Item.delete_item(name)
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        if Item.find_by_name(name):
            try:
                Item.update(name, data['price'])
            except:
                return {"message": "Error occurred while updating item"}, 500
        else:
            try:
                Item.insert_new(name, data['price'])
            except:
                return {"message": "Error occurred while inserting new item"}, 500

        return {"name": name, "price": data['price']}

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)
        rows = result.fetchall()
        connection.close()

        return rows

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(select_query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"name": row[0], "price": row[1]}

    @classmethod
    def insert_new(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items VALUES(?,?)"
        result = cursor.execute(insert_query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "UPDATE items SET price = ? WHERE name = ?"
        result = cursor.execute(insert_query, (price, name))
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "DELETE FROM items WHERE name = ?"
        result = cursor.execute(insert_query, (name,))
        connection.commit()
        connection.close()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        items = []
        for r in Item.get_all():
            items.append({"name": r[0], "price": r[1]})

        return {'items': items if items else None}
