from app import db

class Job(db.Model):
    __tablename__ = 'jobs'
    __table_args__ = {'schema': 'hr'}
    job_id = db.Column('job_id', db.String(10), primary_key=True)
    job_title = db.Column('job_title', db.String(80))
    min_salary = db.Column('min_salary', db.Integer, nullable=True)
    max_salary = db.Column('max_salary', db.Integer, nullable=True)

    def __repr__(self):
        return '<Job %r>' % self.job_title

    def job_form_data(self, form):
        self.job_id = form.get('job_id')
        self.job_title = form.get('job_title')
        self.min_salary = form.get('min_salary')
        self.max_salary = form.get('max_salary')
        return self

    @property
    def serialize(self):
        return {'job_id': self.job_id,
                'job_title': self.job_title,
                'min_salary': self.min_salary,
                'max_salary': self.max_salary
                }


class Employee(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'hr'}
    employee_id = db.Column('employee_id', db.String(10), db.ForeignKey('hr.employees.employee_id'), primary_key=True)
    manager = db.relationship('Employee', remote_side=[employee_id])
    first_name = db.Column('first_name', db.String(20))
    last_name = db.Column('last_name', db.String(25))
    email = db.Column('email', db.Text, unique=True)
    phone_number = db.Column('phone_number', db.String(20), nullable=True)
    hire_date = db.Column('hire_date',db.DateTime)
    job_id = db.Column('job_id', db.String(10), db.ForeignKey('hr.jobs.job_id'), nullable=False, primary_key=True)
    job = db.relationship('Job')
    salary = db.Column('salary', db.Float(precision='10,2'), nullable=False)
    commission_pct = db.Column('commission_pct', db.Float(precision='2,2'), nullable=False)
    department_id = db.Column('department_id',db.Integer, nullable=True)

    def __repr__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def employee_form_data(self, form):
        self.employee_id = form.get('employee_id')
        self.first_name = form.get('first_name')
        self.last_name = form.get('last_name')
        self.phone_number = form.get('phone_number')
        self.hire_date = form.get('hire_date')
        self.job_id = form.get('job_id')
        self.salary = form.get('salary')
        self.commission_pct = form.get('commission_pct')
        self.email = form.get('email')
        return self

    @property
    def serialize(self):
        return {'employee_id': self.employee_id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'phone_number': self.phone_number,
                'hire_date': self.hire_date,
                'job_id': self.job_id,
                'salary': self.salary,
                'commission_pct': self.commission_pct,
                'department_id': self.department_id
                }



class JobHistory(db.Model):
    __tablename__ = 'job_history'
    __table_args__ = {'schema': 'hr'}
    employee_id = db.Column('employee_id', db.String(10), db.ForeignKey('hr.employees.employee_id'), primary_key=True)
    employee = db.relationship('Employee')
    start_date = db.Column('start_date',db.DateTime)
    end_date = db.Column('end_date',db.DateTime)
    job_id = db.Column('job_id', db.String(10), db.ForeignKey('hr.jobs.job_id'), nullable=False, primary_key=True)
    job = db.relationship('Job')
    department_id = db.Column('department_id', db.Integer, nullable=True)

    def __repr__(self):
        return '%s %s %s' % (self.employee_id, self.job_id, self.department_id)

    @property
    def serialize(self):
        return {'employee_id': self.employee_id,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'job_id': self.job_id,
                'department_id': self.department_id
                }

class Country(db.Model):
    __tablename__ = 'countries'
    __table_args__ = {'schema': 'hr'}
    country_id = db.Column('country_id', db.String(2), primary_key=True)
    country_name = db.Column('country_name', db.String(40))
    region_id = db.Column('region_id', db.Integer)

    @property
    def serialize(self):
        return {'country_id': self.country_id,
                'country_name': self.country_name,
                'region_id': self.region_id
                }

    def department_form_data(self, form):
        self.country_id = form.get('country_id')
        self.country_name = form.get('country_name')
        self.region_id = form.get('region_id')
        return self

    def __repr__(self):
        return '%s' % (self.country_name)


class Department(db.Model):
    __tablename__ = 'departments'
    __table_args__ = {'schema': 'hr'}
    department_id = db.Column('department_id', db.Integer, primary_key=True)
    department_name = db.Column('department_name', db.String(30))
    manager_id = db.Column('manager_id', db.Integer, db.ForeignKey('hr.employees.employee_id'))
    manager= db.relationship('Employee')
    location_id = db.Column('location_id', db.Integer, db.ForeignKey('hr.locations.location_id'))

    @property
    def serialize(self):
        return {'department_id': self.department_id,
                'department_name': self.department_name,
                'manager_id': self.manager_id,
                'location_id': self.location_id
                }

    def department_form_data(self, form):
        self.department_id = form.get('department_id')
        self.department_name = form.get('department_name')
        self.manager_id = form.get('manager_id')
        self.location_id = form.get('location_id')
        return self

    def __repr__(self):
        return '%s' % (self.department_name)


class Location(db.Model):
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'hr'}
    location_id = db.Column('location_id', db.Integer, primary_key=True)
    street_address = db.Column('street_address', db.String(40))
    postal_code = db.Column('postal_code', db.String(12))
    city = db.Column('city', db.String(30))
    state_province = db.Column('state_province', db.String(25))
    country_id = db.Column('country_id', db.String(2), db.ForeignKey('hr.countries.country_id'))
    country = db.relationship('Country')


    @property
    def serialize(self):
        return {'location_id': self.location_id,
                'street_address': self.street_address,
                'postal_code': self.postal_code,
                'city': self.city,
                'state_province': self.state_province,
                'country_id': self.country_id
                }

    def department_form_data(self, form):
        self.location_id = form.get('location_id')
        self.street_address = form.get('street_address')
        self.postal_code = form.get('postal_code')
        self.city = form.get('city')
        self.state_province = form.get('state_province')
        self.country_id = form.get('country_id')
        return self

    def __repr__(self):
        return '%s (%s)' % (self.city, self.location_id)

