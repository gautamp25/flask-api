from flask import Flask, request, Blueprint, jsonify, json
from flask_restful import Resource, Api
from assets_api.api import app,db
from assets_api.models import Organization, Department,department_schema
from datetime import datetime


department = Blueprint('department', __name__)
api = Api(department)


class DepartmentResource(Resource):
    def get(self):
        dept_name = Department.query.all()
        result = department_schema.dump(dept_name)
        return jsonify({"Department": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            try:
                org_id = Organization.query.filter(Organization.organization_name == data['orgname']).first()
                # print('************',org_id.id)
                dept = Department(data['dp_name'], org_id.id)
                Department.save_data(dept)
                success = {"message": "Department created successfully"}
                
            except:
                return {'message': 'Something went wrong'}, 400
            return success, 201
        else:
            return {'message': 'Something went wrong'}


api.add_resource(DepartmentResource, '/api/department')
app.register_blueprint(department)



