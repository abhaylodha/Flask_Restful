import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users where id = ?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This cannot be left blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This cannot be left blank.")

    @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "User already exists with this name."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(insert_query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"message": "User created successfully."}, 201
