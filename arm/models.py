import os.path

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base, engine
from . import app

import datetime

from flask_login import UserMixin

# User object model
class User(Base, UserMixin):
    __tablename__ = "users"

	# User db table fields
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

# Asset object model
class Asset(Base):
	__tablename__ = 'assets'

	# Asset db table fields
	id = Column(Integer, primary_key = True)
	barcode = Column(String, nullable = False, unique = True)
	serial_no = Column(String, nullable = True)
	capture_date = Column(DateTime, default = datetime.datetime.now)
	name = Column(String(128), nullable = False)
	ccategory = Column(Integer, ForeignKey('asset_categories.id'), nullable = True)
	_type = Column(Integer, ForeignKey('asset_types.id'), nullable = True)
	_model = Column(Integer, ForeignKey('asset_models.id'), nullable = True)
	status = Column(Integer, ForeignKey('asset_status.id'), nullable = True)
	location = Column(Integer, ForeignKey('locations.id'), nullable = True)
	user = Column(Integer, ForeignKey('people.id'), nullable = True)
	purchase_price = Column(Integer, nullable = True)
	value = Column(Integer, nullable = True)
	supplier = Column(Integer, ForeignKey('suppliers.id'), nullable = True)
	photo = Column(String, nullable = True)
	comments = Column(String(256), nullable = True)

	#Return asset object as dictionary
	def as_dictionary(self):
		asset={"Id": self.id, "Barcode": self.barcode, "Serial No.": self.serial_no,
				"Capture Date": self.capture_date, "Name": self.name, "Category": self.category,
				"Type": self._type, "Model": self._model, "Status": self.status,
				"Location": self.location, "User": self.user, "Purchase Price": self.purchase_price,
				"Value": self.value, "Supplier": self.supplier, "Photo": self.photo,
				"Comments": self.comments
				}
		return asset


# Asset Category object model
class AssetCategory(Base):
	__tablename__ = 'asset_categories'

	# Asset category db table fields
	id = Column(Integer, primary_key = True)
	category_code = Column(String(128), nullable = False, unique = True)
	category_name = Column(String(128), nullable = False, unique = True)
	comments = Column(String(256), nullable = True)
	# category_assets = relationship("Asset", backref = "asset_category")

	# Return asset category object as dictionary
	def as_dictionary(self):
		categories = {"id": self.id, "Category Name": self.category_name}
		return categories

# Asset Type object model
class AssetType(Base):
	__tablename__ = 'asset_types'

	# Asset type db table fields
	id = Column(Integer, primary_key = True)
	type_name = Column(String(128), nullable = False, unique = True)
	type_assets = relationship ("Asset", backref = "asset_type")

	# Return asset type object as dictionary
	def as_dictionary(self):
		_types = {"id": self.id, "type_name": self.type_name}
		return _types

# Asset Model object model
class AssetModel(Base):
	__tablename__ = 'asset_models'

	# Asset model db table fields
	id = Column(Integer, primary_key = True)
	model_name = Column(String(128), nullable = False, unique = True)
	model_assets = relationship ("Asset", backref = "asset_model")

	# Return asset model object as dictionary
	def as_dictionary(self):
		_models = {"id": self.id, "model_name": self.model_name}
		return _models

# Asset Status object model
class AssetStatus(Base):
	__tablename__ = 'asset_status'

	# Asset status db table fields
	id = Column(Integer, primary_key = True)
	status_code = Column(String(64), nullable = False, unique = True)
	status_name = Column(String(128), nullable = False, unique = True)
	status_assets = relationship ("Asset", backref = "asset_status")

	# Return asset status object as dictionary
	def as_dictionary(self):
		_status ={"id": self.id, "status_code": self.status_code, 
					"status_name": self.status_name
					}
		return _status

# Asset Location object model
class Location(Base):
	__tablename__ = 'locations'

	# Asset location db table fields
	id = Column(Integer, primary_key = True)
	location_code = Column(String(64), nullable = False, unique = True)
	location_name = Column(String(128), nullable = False)
	category = Column(Integer, ForeignKey("location_categories.id"), nullable = True)
	location_assets = relationship ("Asset", backref = "asset_location")
	location_people = relationship ("People", backref = "person_location")

	# Return asset locations object as dictionary
	def as_dictionary(self):
		_locations ={"id": self.id, "location_code": self.location_code,
					"location_name": self.location_name,
					"category": self.category
					}
		return _locations

# Asset Location Category object model
class LocationCategory(Base):
	__tablename__ = 'location_categories'

	# Asset locations categories db table fields
	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_locations = relationship ("Location", backref = "location_category")

	# Return asset locations categories as dictionary
	def as_dictionary(self):
		_locations_categories = {"id": self.id, "category_name": self.category_name}
		return _locations_categories

# People object model
class People(Base):
	__tablename__ = 'people'

	# People db table fields
	id = Column(Integer, primary_key = True)
	barcode = Column(String(64), nullable = False, unique = True)
	category = Column(Integer, ForeignKey("people_categories.id"), nullable = False)
	first_name = Column(String(128), nullable = False)
	last_name = Column(String(128), nullable = False)
	designation = Column(String(128), nullable = True)
	department = Column(Integer, ForeignKey("departments.id"), nullable = False)
	location = Column(Integer, ForeignKey("locations.id"), nullable = False)
	phone = Column(Integer, unique = True)
	email = Column(String(128), unique = True)

	# Return people as dictionary
	def as_dictionary(self):
		_people = {"id": self.id, "Barcode": self.barcode, "Category": self.category, 
					"First Name": self.first_name, "Last Name": self.last_name, 
					"Designation": self.designation, "Department": self.department, 
					"Location": self.location, "Phone": self.phone, "Email": self.email
					}
		return _people

# People Category object model
class PeopleCategory(Base):
	__tablename__ = 'people_categories'

	# People category db table fields
	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_people = relationship ("People", backref = "person_category")

	# Return People categories as dictionary
	def as_dictionary(self):
		people_category = {"id": self.id, "category_name": self.category_name}
		return people_category

# Department object model
class Department(Base):
	__tablename__ = "departments"

	# Department db table fields
	id = Column(Integer, primary_key = True)
	department_code = Column(String(64), nullable = True, unique = True)
	department_name = Column(String(128), nullable = False)
	department_people = relationship ("People", backref = "person_department")

	# Return departments as dictionary
	def as_dictionary(self):
		_departments = {"id": self.id, "department_code": self.department_code,
								"department_name": self.department_name
								}
		return _departments

# Supplier object model
class Supplier(Base):
	__tablename__ = 'suppliers'

	# Supplier db table fields
	id = Column(Integer, primary_key = True)
	code = Column(String(64), nullable = False, unique = True)
	category = Column(Integer, ForeignKey("suppliers_category.id"), nullable = False)
	phone = Column(Integer, nullable = False, unique = True)
	email = Column(String(128), unique = True)
	location = Column(Integer, ForeignKey("locations.id"), nullable = False)
	website = Column(String(128), nullable = True, unique = True)
	person = Column(Integer, ForeignKey("people.id"), nullable = True)

	# Return suppliers as dictionary
	def as_dictionary(self):
		_suppliers = {"id": self.id, "code": self.code, "category": self.category,
						"phone": self.phone, "email": self.email, "location": self.location,
						"website": self.website
						}
		return _suppliers

# Supplier category model
class SupplierCategory(Base):
	__tablename__ = 'suppliers_category'

	# Supplier category db table fields
	id = Column(Integer, primary_key = True)
	category_name = Column(String(128), nullable = False, unique = True)
	category_suppliers = relationship ("Supplier", backref = "supplier_category")

	# Return supplier categories as dictionary
	def as_dictionary(self):
		supplier_categories = {"id": self.id, "category_name": self.category_name}
		return supplier_categories