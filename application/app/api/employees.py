from flask import jsonify, request
from flask import views

from app import db
from models import Employee

from datetime import datetime

class EmployeesApi(views.MethodView):

    def get(self):
        return jsonify([a.serialize for a in Employee.query.all()])

    def post(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        if (len(data.get('job_id')) == 0
                or len(data.get('first_name')) == 0
                or len(data.get('last_name')) == 0
                or len(data.get('hire_date')) == 0
                or len(str(data.get('salary'))) == 0
                or int(data.get('salary')) == 0
                or len(str(data.get('commission_pct'))) == 0
                or len(data.get('email')) == 0
                or data.get('department_id') == 0):

            return jsonify({'message': 'Preencha todos os campos.'}), 409


        newEmployee = Employee().employee_form_data(data)
        newEmployee.employee_id = Employee.query.order_by(Employee.employee_id.desc()).first().employee_id + 1
        newEmployee.hire_date = datetime.strptime(data.get('hire_date'), '%Y-%m-%d %H:%M:%S')
        db.session.add(newEmployee)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Employee inserido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500

    def put(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        print(data)

        if (len(data.get('job_id')) == 0
                or len(data.get('first_name')) == 0
                or len(data.get('last_name')) == 0
                or len(data.get('hire_date')) == 0
                or len(str(data.get('salary'))) == 0
                or int(data.get('salary')) == 0
                or len(str(data.get('commission_pct'))) == 0
                or len(data.get('email')) == 0
                or data.get('department_id') == 0):
            return jsonify({'message': 'Preencha todos os campos.'}), 409

        editedEmployee = Employee.query.filter_by(employee_id=data.get('employee_id')).first()
        editedEmployee.job_title = data.get('job_title')
        editedEmployee.first_name = data.get('first_name')
        editedEmployee.last_name = data.get('last_name')
        # editedEmployee.hire_date = datetime.strptime(data.get('hire_date'), '%Y-%m-%d %H:%M:%S')
        editedEmployee.phone_number = data.get('phone_number')
        editedEmployee.salary = data.get('salary')
        editedEmployee.commission_pct = data.get('commission_pct')
        editedEmployee.department_id = data.get('department_id')
        editedEmployee.email = data.get('email')

        db.session.add(editedEmployee)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Employee atualizado.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500

    def delete(self, id):

        Employee.query.filter_by(employee_id=id).delete()

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Employee removido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500
