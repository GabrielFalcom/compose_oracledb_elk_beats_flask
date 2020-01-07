import json

from flask import jsonify, views

from app import db
from models import Country, Department, Location, Employee


class FuzzyApi(views.MethodView):

    def get(self,country_id=None, department_id=None,city=None):
        if country_id and not department_id:
            departmentsCountry = db.session.query(Department, Location, Country, Employee) \
                .filter(Country.country_id == Location.country_id) \
                .filter(Department.location_id == Location.location_id) \
                .filter(Employee.department_id == Department.department_id) \
                .filter(Country.country_id == country_id) \
                .all()

            json = []
            for department, location, country, employee in departmentsCountry:
                dictResult = {}
                dictResult.update(department.serialize)
                dictResult.update(location.serialize)
                dictResult.update(country.serialize)
                dictResult.update(employee.serialize)
                json.append(dictResult)

            return jsonify(json)

        elif country_id and department_id and not city:
            departmentsCountry = db.session.query(Department, Location, Country, Employee) \
                .filter(Country.country_id == Location.country_id) \
                .filter(Department.location_id == Location.location_id) \
                .filter(Employee.department_id == Department.department_id) \
                .filter(Country.country_id == country_id) \
                .filter(Department.department_id == department_id) \
                .all()

            json = []
            for department, location, country, employee in departmentsCountry:
                dictResult = {}
                dictResult.update(department.serialize)
                dictResult.update(location.serialize)
                dictResult.update(country.serialize)
                dictResult.update(employee.serialize)
                json.append(dictResult)

            return jsonify(json)


        elif country_id and department_id and city:
            departmentsCountry = db.session.query(Department, Location, Country, Employee) \
                .filter(Country.country_id == Location.country_id) \
                .filter(Department.location_id == Location.location_id) \
                .filter(Employee.department_id == Department.department_id) \
                .filter(Department.department_id == department_id) \
                .filter(Country.country_id == country_id) \
                .filter(Location.city == city) \
                .all()

            json = []
            for department, location, country, employee in departmentsCountry:
                dictResult = {}
                dictResult.update(department.serialize)
                dictResult.update(location.serialize)
                dictResult.update(country.serialize)
                dictResult.update(employee.serialize)
                json.append(dictResult)

            return jsonify(json)
        else:
            result = db.session.execute("SELECT COUNTRY_NAME, CITY, DEPARTMENT_NAME, FIRST_NAME FROM HR.COUNTRIES JOIN HR.LOCATIONS USING (COUNTRY_ID) JOIN HR.DEPARTMENTS USING (LOCATION_ID) JOIN HR.EMPLOYEES E on HR.DEPARTMENTS.DEPARTMENT_ID = E.DEPARTMENT_ID")
            jsonDict = ([(dict(row.items())) for row in result])
            return jsonify(jsonDict)