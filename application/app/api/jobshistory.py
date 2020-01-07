from flask import jsonify
from flask import views

from app import db
from models import JobHistory

class JobsHistoryApi(views.MethodView):

    def get(self):
        return jsonify([a.serialize for a in JobHistory.query.all()])

    def delete(self, id):
        JobHistory.query.filter_by(employee_id=id).delete()

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Job History removido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500