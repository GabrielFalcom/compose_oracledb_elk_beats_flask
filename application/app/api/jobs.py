from flask import jsonify, views, request

from app import db
from models import Job

class JobsApi(views.MethodView):

    def get(self):
        return jsonify([a.serialize for a in Job.query.all()])

    def post(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        if (len(data.get('job_id')) == 0
                or len(data.get('job_title')) == 0
                or len(str(data.get('min_salary'))) == 0
                or int(data.get('min_salary')) == 0
                or len(str(data.get('max_salary'))) == 0
                or int(data.get('max_salary')) == 0):

            return jsonify({'message': 'Preencha todos os campos.'}), 409


        newJob = Job().job_form_data(data)
        db.session.add(newJob)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Job inserido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500

    def put(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        print(data)

        if (len(data.get('job_id')) == 0
            or len(data.get('job_title')) == 0
            or len(str(data.get('min_salary'))) == 0
            or int(data.get('min_salary')) == 0
            or len(str(data.get('max_salary'))) == 0
            or int(data.get('max_salary')) == 0):

            return jsonify({'message': 'Preencha todos os campos.'}), 409

        editedJob = Job.query.filter_by(job_id=data.get('job_id')).first()
        editedJob.job_title = data.get('job_title')
        editedJob.min_salary = data.get('min_salary')
        editedJob.max_salary = data.get('max_salary')

        db.session.add(editedJob)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Job atualizado.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500

    def delete(self, id):

        Job.query.filter_by(job_id=id).delete()

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Job removido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500