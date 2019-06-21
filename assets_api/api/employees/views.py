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
            joindate = datetime.strptime(data['doj'], '%Y-%m-%d')
            # print('***********', username, password, department, joindate)

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


class EmployeeRes(Resource):

        def get(self, id):
            try:
                emp_details = Employee.query.filter_by(id=id)

                result = employee_schema.dump(emp_details)
                return jsonify({"Employee": result.data})
            except Exception as e:
                print('Error', e)
                return {'Not Found': 'Record not found.'}, 404


api.add_resource(EmployeeResource, '/api/employee')
api.add_resource(EmployeeRes, '/api/employee/<int:id>')
app.register_blueprint(employee_bp)



