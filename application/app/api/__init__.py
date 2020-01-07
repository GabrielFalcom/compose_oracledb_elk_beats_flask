import  flask

from  .. import app
from .jobs import JobsApi
from .employees import EmployeesApi
from .jobshistory import JobsHistoryApi
from .contries import CountryApi
from .departments import DepartmentApi
from .locations import LocationApi
from .fuzzy import FuzzyApi
api = flask.Blueprint('api', __name__)

add_url = api.add_url_rule

jobs_view = JobsApi.as_view('jobs')
add_url('/jobs', view_func=jobs_view, methods=['GET', 'POST', 'DELETE','PUT'])
add_url('/jobs/<id>', view_func=jobs_view, methods=['GET', 'PUT', 'DELETE'])

employees_view = EmployeesApi.as_view('employees')
add_url('/employees', view_func=employees_view, methods=['GET', 'POST', 'DELETE','PUT'])
add_url('/employees/<id>', view_func=employees_view, methods=['GET', 'PUT', 'DELETE'])

jobs_history_view = JobsHistoryApi.as_view('jobshistory')
add_url('/jobshistory', view_func=jobs_history_view, methods=['GET', 'POST', 'DELETE','PUT'])
add_url('/jobshistory/<id>', view_func=jobs_history_view, methods=['GET', 'PUT', 'DELETE'])

departments_view = DepartmentApi.as_view('departments')
add_url('/departments', view_func=departments_view, methods=['GET', 'POST', 'DELETE','PUT'])
# add_url('/departments/<id>', view_func=departments_view, methods=['GET', 'PUT', 'DELETE'])
add_url('/departments/<country_id>', view_func=departments_view, methods=['GET'])

countries_view = CountryApi.as_view('countries')
add_url('/countries', view_func=countries_view, methods=['GET', 'POST', 'DELETE','PUT'])
# add_url('/countries/<id>', view_func=countries_view, methods=['GET', 'PUT', 'DELETE'])
add_url('/countries/<country_id>/<city>', view_func=countries_view, methods=['GET'])

locations_view = LocationApi.as_view('locations')
add_url('/locations', view_func=locations_view, methods=['GET', 'POST', 'DELETE','PUT'])
add_url('/locations/<id>', view_func=locations_view, methods=['GET', 'PUT', 'DELETE'])

fuzzy_view = FuzzyApi.as_view('fuzzy')
add_url('/fuzzy', view_func=fuzzy_view, methods=['GET'])
add_url('/fuzzy/<country_id>', view_func=fuzzy_view, methods=['GET'])
add_url('/fuzzy/<country_id>/<department_id>', view_func=fuzzy_view, methods=['GET'])
add_url('/fuzzy/<country_id>/<department_id>/<city>', view_func=fuzzy_view, methods=['GET'])

app.register_blueprint(api, url_prefix='/api')

app.config["JSON_SORT_KEYS"] = False