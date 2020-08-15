# -*- coding: utf-8 -*-

"""
Main Engine of Sail Outreach
~~~~~~~~~~~~
With Flask this provides a webapp for outreach usage.
:by Leonardo Galindo 2020 
:license: Apache2, see LICENSE for more details.
"""
import sys
from os import path
sys.path.append('src/')
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from file_processing import pandas_file_handler, pandas_to_sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
db = SQLAlchemy(app)

class Schools(db.Model):
    __tablename__ = "School"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    st_abrv = db.Column(db.String(3), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    school_type = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(16), nullable=False)
    num_of_students = db.Column(db.Integer)
    percent_bl = db.Column(db.Integer)
    percent_as = db.Column(db.Integer)
    percent_his = db.Column(db.Integer)
    percent_nat = db.Column(db.Integer)
    percent_paci = db.Column(db.Integer)
    percent_whit = db.Column(db.Integer)
    percent_two = db.Column(db.Integer)
    percent_low = db.Column(db.Integer)
    percent_male = db.Column(db.Integer)
    percent_fem = db.Column(db.Integer)

    def __repr__(self):
        return '<School %s, %s - %s - %s%% - %s%% - %s%% - %s%%>' % (
                self.name, self.city, self.state, 
                self.num_of_students, self.percent_bl, 
                self.percent_as, self.percent_his
            )

#TODO: Check the website every certain year date when databse is updated
if not path.exists("schools.db"):
    pandas_to_sql(pandas_file_handler(), db)

@app.route('/',  methods=['POST', 'GET'])
def index():
    # Added an extra space to accomodate for IL Abbrevation
    # TODO: Add options of choosing certain states!
    schools = Schools.query.filter(Schools.st_abrv == "IL" + " ").order_by(Schools.num_of_students.desc()).all()
    if request.method == "POST":
        select_filter = request.form['sel-filter']
        filter_percent_input = ""
        filter_ = None
        try:
            filter_percent_input = request.form['percent-filter']
            filter_percent, filter_ = get_school_col(int(select_filter))
        except:
            filter_percent, filter_ = get_school_col(int(select_filter))

        if filter_percent_input != "":
            filter_percent = filter_percent_input

        try:
            request.form['ascending']
            is_ascending = True
        except:
            is_ascending = False

        if is_ascending:
            schools = (
                Schools.query.filter(filter_ > filter_percent)
                .order_by(Schools.num_of_students)
                .all())
        else:
            schools = (
                Schools.query.filter(filter_ > filter_percent)
                .order_by(Schools.num_of_students.desc())
                .all())
    else:
        print("Get Request Made")

    return render_template('index.html', schools=schools)

def get_school_col(filter_input):
    if filter_input == 1:
        return 30, Schools.percent_whit
    elif filter_input == 2:
        return 20, Schools.percent_af
    elif filter_input == 3:
        return 10, Schools.percent_as
    elif filter_input == 4:
        return .01, Schools.percent_nat
    elif filter_input == 5:
        return 20, Schools.percent_his
    elif filter_input == 6:
        return .01, Schools.percent_paci
    elif filter_input == 7:
        return .01, Schools.percent_two
    elif filter_input == 8:
        return 40, Schools.percent_free
    else:
        return 0, Schools.num_of_students

if __name__ == "__app__":
    app.run(debug=True)