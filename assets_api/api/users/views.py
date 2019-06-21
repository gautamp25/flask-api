from flask import Flask, request, Blueprint, jsonify, json
from flask_restful import Resource, Api
from assets_api.api import app,db
from assets_api.models import User,user_schema
from datetime import datetime
import requests


user_bp = Blueprint('user_bp', __name__)
api = Api(user_bp)


class UserResource(Resource):
    def get(self):
        all_user = User.query.all()
        result = user_schema.dump(all_user)
        return jsonify({"User": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            username = data['username']
            password = data['password']
            user = User(username, password)
            User.save_data(user)
            return {'success': 'User creation successful!'}, 201
        else:
            return {'message': 'Something went wrong'}


obj_user = UserResource()

class UserRes(Resource):

    def delete(self, name):
        print("*******************",name)
        try:
            org = User.query.filter_by(id=1).first()
            # result = organization_schema.dump(org)
            # org_id = json.dump(org.id)
            print('********',org, org.id)
            # department = Department.query.filter_by(organization_id=org.id).first()
            # print(department.id)
            db.session.delete(org.id)
            # db.session.delete(department.id)
            db.session.commit()
        except:
            return {'message': 'Something went wrong'}, 400
        return {'Success': 'User delete successful'},200


api.add_resource(UserResource, '/api/user')
# api.add_resource(UserRes, '/api/user/<string:name>')
app.register_blueprint(user_bp)



