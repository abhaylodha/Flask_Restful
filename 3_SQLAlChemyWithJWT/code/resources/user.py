from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.user import UserModel


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
        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists with this name."}, 400
        UserModel(**data).save_to_db()
        # Same as below
        #UserModel(data['username'], data['password']).save_to_db()
        return {"message": "User created successfully."}, 201
