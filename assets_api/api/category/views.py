from flask import request, Blueprint, jsonify, json
from flask_restful import Resource, Api
from assets_api.api import app,db
from assets_api.models import Category, category_schema


category_bp = Blueprint('category_bp', __name__)
api = Api(category_bp)


class CategoryResource(Resource):
    def get(self):
        all_category = Category.query.all()
        result = category_schema.dump(all_category)
        return jsonify({"Category": result.data})

    def post(self):
        data = request.get_json()

        if request.method == "POST":
            category = data['category']
            subcategory = data['subcategory']
            try:
                exists = Category.query.filter_by(category=category).scalar() is not None
                if exists:
                    return {'error': 'Category already exists'}
                else:
                    category = Category(category, subcategory)
                    Category.save_category(category)
                    return {'success': 'Category creation successful!'}, 201
            except None:
                return {'error': 'Error occurred while category creation...'}
        else:
            return {'message': 'Something went wrong'}




class CategoryRes(Resource):

    def delete(self, name):
        print("*******************",name)
        try:
            cat = Category.query.filter_by(id=1).first()
            # result = organization_schema.dump(org)
            # org_id = json.dump(org.id)
            # print('********',org, org.id)
            # department = Department.query.filter_by(organization_id=org.id).first()
            # print(department.id)
            db.session.delete(cat.id)
            # db.session.delete(department.id)
            db.session.commit()
        except:
            return {'message': 'Something went wrong'}, 400
        return {'Success': 'Category delete successful'},200



api.add_resource(CategoryResource, '/api/category')
api.add_resource(CategoryRes, '/api/category/<string:name>')
app.register_blueprint(category_bp)



