import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

#######################
### DATABASE SETUP ####
#######################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACk_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

from assets_api.api.orgnizations.views import organization
from assets_api.api.department.views import department
from assets_api.api.users.views import user_bp
from assets_api.api.employees.views import employee_bp
from assets_api.api.category.views import category_bp
from assets_api.api.assets.views import asset_bp
# from assets_api.api.assets.views import assignasset_bp

# app.register_blueprint(organization)


