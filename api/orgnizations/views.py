from flask import Flask, request, Blueprint, jsonify
from flask_restful import Resource, Api
from assets_api.api import app,db
from assets_api.models import Organization



organization = Blueprint('organization', __name__)
api = Api(organization)

org_list = []

@organization.route('/')
def index():
    return "<h1>Welcome to RESTful Page.</h1>"


class Organization(Resource):
    def get(self):
        print("*"*10, org_list)
        # org_dict={'name':'Nitor'}
        for org_name in org_list:
            if org_name['name']:
                return org_name
        return {'name':None}, 404
        # return org_dict

    def post(self):
        print("FGHJKL:")
        print(request.form['name'])
        print(request.form.get('country'))
        print(request.form['city'])
        print(request.form['is_active'])
        if request.method == 'POST':
            org_name = request.form['name']
            country = request.form['country']
            city = request.form['city']
            # created_date = request.form['name']
            is_active = request.form['is_active']
            # org_list.append(org_name)
            print(org_name,country,city,is_active)
            pup = Organization(organization_name=org_name, country=country,city=city, is_active=is_active )
            db.session.add(pup)
            db.session.commit()
            print('PUP',pup)
            return pup, 201


api.add_resource(Organization, '/api/organization') # '/api/organization/<string:name>'
app.register_blueprint(organization)



