from flask import jsonify, views, request

from app import db
from models import Department, Location, Country


class DepartmentApi(views.MethodView):

    def get(self, country_id=None):
        if not country_id:
            return jsonify([a.serialize for a in Department.query.all()])
        else:
            departmentsCountry = db.session.query(Department,Location,Country)\
                .filter(Country.country_id == Location.country_id)\
                .filter(Department.location_id == Location.location_id)\
                .filter(Country.country_id == country_id)\
                .all()

            json = []
            for department, location, country in departmentsCountry:
                dict = {}
                dict.update(department.serialize)
                dict.update(location.serialize)
                dict.update(country.serialize)
                json.append(dict)

            return jsonify(json)


    def post(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        if(len(str(data.get('department_id'))) == 0
          or int(data.get('department_id')) == 0
          or len(data.get('department_name')) == 0):

            return jsonify({'message': 'Informe o Dpt ID e Dpt Name.'}), 409


        departmentID = Department.query.filter_by(department_id=data.get('department_id')).first()
        managerID = None

        if data.get('manager_id') != None:
            managerID = Department.query.filter_by(manager_id=data.get('manager_id')).first()

        if departmentID:
            return jsonify({'message': 'Dpt ID já cadastrado.'}), 409

        if managerID:
            return jsonify({'message': 'Manager ID já cadastrado.'}), 409


        department = Department().department_form_data(data)

        db.session.add(department)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Department inserido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500

    def put(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        if (len(str(data.get('department_id'))) == 0
                or int(data.get('department_id')) == 0
                or len(data.get('department_name')) == 0):
            return jsonify({'message': 'Informe o Dpt ID e Dpt Name.'}), 409

        editedDepartment = Department.query.filter_by(department_id=data.get('department_id')).first()
        editedDepartment.department_name = data.get('department_name')
        editedDepartment.manager_id = data.get('manager_id')
        editedDepartment.location_id = data.get('location_id')

        db.session.add(editedDepartment)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Department atualizado.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500


    def delete(self, id):
        Department.query.filter_by(department_id=id).delete()

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Department removido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500