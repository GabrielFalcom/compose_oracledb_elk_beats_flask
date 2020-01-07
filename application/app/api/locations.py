from flask import jsonify, views
from models import Location

class LocationApi(views.MethodView):

    def get(self):
        return jsonify([a.serialize for a in Location.query.all()])