from flask import Flask, request, Blueprint, jsonify, json
from flask_restful import Resource, Api
from assets_api.api import app, db
from assets_api.models import Organization, organization_schema, Department
from datetime import datetime
import requests


organization = Blueprint('organization', __name__)
api = Api(organization)

org_list = []


@organization.route('/')
def index():
    return "<h1>Welcome to RESTful Page.</h1>"


class OrganizationResource(Resource):
    def get(self):
        org_name = Organization.query.all()
        result = organization_schema.dump(org_name)
        return jsonify({"Organization": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            org_name = data['name']
            country = data['country']
            city = data['city']
            created_date = datetime.now()
            is_active = data['is_active']
            org = Organization(org_name, country, city, created_date, is_active)
            Organization.save_data(org)
            return 'Done', 201
        else:
            return {'message':'Something went wrong'}


class OrganizationRes(Resource):
    def get(self, id):
        print(id)
        try:
            org_details = Organization.query.filter_by(id=id)
            print(Org_details)
            result = organization_schema.dump(org_details)
            return jsonify({"Organization": result.data})
        except Exception as e:
            print('Error', e)
            return {'Not Found': 'Record not found.'}, 404

    def delete(self, id):
        print("*******************",id)
        try:
            org = Organization.query.filter_by(id=1).first()
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
        return {'Success': 'Organization delete successful'},200


api.add_resource(OrganizationResource, '/api/organization')
api.add_resource(OrganizationRes, '/api/organization/<int:id>')
app.register_blueprint(organization)



