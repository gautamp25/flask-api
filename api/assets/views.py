from flask import Flask, request, Blueprint, jsonify, json
from flask_restful import Resource, Api
from assets_api.api import app,db
from assets_api.models import Asset, Category, Organization, AssignedAsset, User, asset_schema, assignasset_schema
from datetime import datetime

asset_bp = Blueprint('asset_bp', __name__)
# assignasset_bp = Blueprint('assignasset_bp', __name__)
api = Api(asset_bp)


class AssetResource(Resource):
    def get(self):
        all_assets = Asset.query.all()
        result = asset_schema.dump(all_assets)
        return jsonify({"Assets": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            asset_name = data['asset_name']
            price = data['price']
            description = data['description']
            serial_no = data['serial_no']
            purchase_date = datetime.today() #data['purchase_date']
            is_dead = data['is_dead']
            category = data['category']
            organization = data['organization']

            try:
                get_organization = Organization.query.filter_by(organization_name=organization).first()

                get_category = Category.query.filter_by(category=category).first()

                asset = Asset(asset_name, price, description, serial_no,
                              purchase_date, is_dead, get_category.id, get_organization.id)

                Asset.save_asset(asset)
                return {'success': 'Asset creation successful!'}, 201
            except:
                return {'message': 'category/organization not exist'}, 400


            # cr_category = Category(category, 1)
            # print('Category', cr_category)
            # db.session.add(cr_category)
            # db.session.commit()


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


class AssignAssetResource(Resource):
    def get(self):
        all_assignedasset = AssignedAsset.query.all()
        result = assignasset_schema.dump(all_assignedasset)
        return jsonify({"Assigned Assets": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            asset_name = data['asset_name']
            user = data['user'].lower()
            employee_id = data['employee_id']
            category = data['category']
            date_assigned = datetime.strptime(data['date_assigned'], '%Y-%m-%d %H:%M:%S')  # data['date_assigned']
            print(date_assigned)
            try:
                get_asset = Asset.query.filter_by(asset_name=asset_name).first()
                get_user = User.query.filter_by(username=user).first()
                get_category = Category.query.filter_by(category=category).first()

                exists = AssignedAsset.query.filter_by(asset_id=get_asset.id, user_id=get_user.id).scalar() is not None
                if exists:
                    return {'message': 'Asset already assigned to this user..'}
                else:
                    assign_asset = AssignedAsset(get_asset.id, get_user.id, employee_id, get_category.id, date_assigned)
                    AssignedAsset.save_assignedasset(assign_asset)
                    return {'success': 'Asset assigned successful!'}, 201
            except Exception as e:
                print(e)
                return {'Error': 'Unable to assign asset.'}, 404


class AssignedAssetRes(Resource):
    def get(self, name):

        try:
            userid = User.query.filter_by(username=name).first()
            all_assignedasset = AssignedAsset.query.filter_by(user_id=userid.id)
            result = assignasset_schema.dump(all_assignedasset)
            return jsonify({"Assigned Assets": result.data})
        except Exception as e:
            print('Error',e)
            return {'Not Found': 'Record not found.'}, 404


api.add_resource(AssetResource, '/api/asset')
api.add_resource(AssignAssetResource, '/api/assign')
api.add_resource(AssignedAssetRes, '/api/assignasset/<string:name>')
app.register_blueprint(asset_bp)
