from assets_api.api import db,app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


# common method
def save_data(self):
    db.session.add(self)
    db.session.commit()


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(70))
    country = db.Column(db.String(50))
    city = db.Column(db.String(70))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    department = db.relationship('Department', backref='department', cascade="all, delete, delete-orphan")

    def __init__(self,organization_name,country,city,created_date,is_active):
        self.organization_name = organization_name
        self.country = country
        self.city = city
        self.created_date = created_date
        self.is_active = is_active

    def save_data(self):
        db.session.add(self)
        db.session.commit()


class OrganizationSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "organization_name", "country", "city", "created_date", "is_active")


organization_schema = OrganizationSchema()
organization_schema = OrganizationSchema(many=True)


# Table departmentt
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    dp_name = db.Column(db.String(80))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, dp_name, organization_id):
        self.dp_name = dp_name
        self.organization_id = organization_id

    def save_data(self):
        db.session.add(self)
        db.session.commit()


class DepartmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("dp_name", "organization_id")


department_schema = DepartmentSchema()
department_schema = DepartmentSchema(many=True)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    employee = db.relationship('Employee', backref='employee', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def save_data(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("username", "password_hash")


user_schema = UserSchema()
user_schema = UserSchema(many=True)


class Employee(db.Model):

    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(70), nullable=False)
    emp_id = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(100))
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    def __init__(self, first_name, last_name, designation, emp_id, address, join_date, user_id, department_id):
        self.first_name = first_name
        self.last_name = last_name
        self.designation = designation
        self.emp_id = emp_id
        self.address = address
        self.join_date = join_date
        self.user_id = user_id
        self.department_id = department_id

    def save_employee(self):
        db.session.add(self)
        db.session.commit()

    # def __repr__(self):
    #     return f"Name {self.first_name} {self.last_name}({self.emp_id}) has designation {self.designation}"


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'designation', 'emp_id', 'address', 'join_date', 'user_id', 'department_id')


employee_schema = EmployeeSchema()
employee_schema = EmployeeSchema(many=True)

class Asset(db.Model):

    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)
    serial_no = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    is_dead = db.Column(db.Boolean, nullable=False, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    organization_id = db.Column(db.Integer,db.ForeignKey('organizations.id'), nullable=False)

    def __init__(self, asset_name, price, description, serial_no, purchase_date, is_dead, category_id, organization_id):
        self.asset_name = asset_name
        self.price = price
        self.description = description
        self.serial_no = serial_no
        self.purchase_date = purchase_date
        self.is_dead = is_dead
        self.category_id = category_id
        self.organization_id = organization_id

    def save_asset(self):
        db.session.add(self)
        db.session.commit()


class AssetSchema(ma.Schema):
    class Meta:
        fields = ('asset_name', 'price', 'description', 'serial_no', 'purchase_date', 'is_dead',
                  'category_id', 'organization_id')


asset_schema = AssetSchema()
asset_schema = AssetSchema(many=True)


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    subcategory = db.Column(db.String(70), nullable=False)

    def __init__(self, category, subcategory):
        self.category = category
        self.subcategory = subcategory

    def save_category(self):
        db.session.add(self)
        db.session.commit()


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("category", "subcategory")


category_schema = CategorySchema()
category_schema = CategorySchema(many=True)


class AssignedAsset(db.Model):

    __tablename__ = 'assigned_assets'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    date_assigned = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, asset_id, user_id, employee_id, category_id, date_assigned):
        self.asset_id = asset_id
        self.user_id = user_id
        self.employee_id = employee_id
        self.category_id = category_id
        self.date_assigned = date_assigned

    def save_assignedasset(self):
        db.session.add(self)
        db.session.commit()


class AssignAssetSchema(ma.Schema):
    class Meta:
        fields = ('asset_id', 'user_id', 'employee_id', 'category_id', 'date_assigned')


assignasset_schema = AssignAssetSchema()
assignasset_schema = AssignAssetSchema(many=True)