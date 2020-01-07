from app import app
from flask import render_template, abort
from models import Job, Employee, JobHistory, Department, Country


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jobs')
def list_jobs():
    return render_template('list_jobs.html', jobs=Job.query.all())

@app.route('/employees')
def list_employees():
    return render_template('list_employees.html', employees=Employee.query.all())

@app.route('/jobshistory')
def list_jobs_history():
    return render_template('list_jobs_history.html', jobHistory=JobHistory.query.all())

@app.route('/departments')
def list_departments():
    return render_template('list_departments.html', departments=Department.query.all())

@app.route('/countries')
def countries():
    return render_template('list_countries.html', countries=Country.query.all())

@app.route('/fuzzy')
def fuzzy():
    return render_template('fuzzy.html')