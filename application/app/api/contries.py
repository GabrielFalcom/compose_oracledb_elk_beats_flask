from flask import jsonify, views, request

from app import db
from models import Country

class CountryApi(views.MethodView):

    def get(self):
        return jsonify([a.serialize for a in Country.query.all()])

    def post(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        if (len(data.get('country_id')) == 0
                or len(data.get('country_name')) == 0
                or len(str(data.get('region_id'))) == 0
                or int(data.get('region_id')) == 0):

            return jsonify({'message': 'Informe todos os campos.'}), 409

        countryID = Country.query.filter_by(country_id=data.get('country_id')).first()

        if countryID:
            return jsonify({'message': 'Country ID já cadastrado.'}), 409

        country = Country().department_form_data(data)

        db.session.add(country)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Country inserido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500

    def put(self):
        if request.json:
            data = request.json
        else:
            data = request.form

        if (len(data.get('country_id')) == 0
                or len(data.get('country_name')) == 0
                or len(str(data.get('region_id'))) == 0
                or int(data.get('region_id')) == 0):
            return jsonify({'message': 'Informe todos os campos.'}), 409

        editedCountry = Country.query.filter_by(country_id=data.get('country_id')).first()
        editedCountry.country_name = data.get('country_name')
        editedCountry.manager_id = data.get('region_id')

        db.session.add(editedCountry)

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Country atualizado.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500


    def delete(self, id):
        Country.query.filter_by(country_id=id).delete()

        try:
            db.session.commit()
            return jsonify(
                {'message': 'Country removido.'})
        except Exception as e:
            return jsonify({'message': 'Não foi possivel executar a operação.'}), 500