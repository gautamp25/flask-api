""" This module handles activities related to Employee """

from flask import Flask, request, Blueprint, jsonify, json
from flask_restful import Resource, Api
from assets_api.api import app,db
from assets_api.models import Employee, employee_schema, Department, User
from assets_api.api.users.views import UserResource,obj_user
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash



employee_bp = Blueprint('employee_bp', __name__)
api = Api(employee_bp)


class EmployeeResource(Resource):
    def get(self):
        all_employee = Employee.query.all()
        result = employee_schema.dump(all_employee)
        return jsonify({"Employees": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            username = data['firstname'].lower()
            password = data['firstname']+'123'
            department = data['department']
            joindate = datetime.today()
            print('***********', username, password, department, joindate)

            try:
                dpname = Department.query.filter_by(dp_name=department).first()
                departmentid = dpname.id
            except :
                return {'message': 'Department not exist'}, 400

            user = User(username, generate_password_hash(password))
            print('USER', user)
            db.session.add(user)
            db.session.commit()

            employee = Employee(data['firstname'], data['lastname'], data['designation'], data['empid'], data['address'],
                                joindate, user.id, departmentid)

            Employee.save_employee(employee)
            return {'success': 'Employee creation successful!'}, 201
        else:
            return {'message': 'Something went wrong'}


# class EmployeeRes(Resource):
#
#     def delete(self, name):
#         try:
#             org = Employee.query.filter_by(id=1).first()
#             # result = organization_schema.dump(org)
#             # org_id = json.dump(org.id)
#             print('********',org, org.id)
#             # department = Department.query.filter_by(organization_id=org.id).first()
#             # print(department.id)
#             db.session.delete(org.id)
#             # db.session.delete(department.id)
#             db.session.commit()
#         except:
#             return {'message': 'Something went wrong'}, 400
#         return {'Success': 'User delete successful'},200


api.add_resource(EmployeeResource, '/api/employee')
# api.add_resource(EmployeeRes, '/api/employee/<string:name>')
app.register_blueprint(employee_bp)



