from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools.db'
db = SQLAlchemy(app)

# TODO
# Create the Visual which will simply just display a rank. Later I can add some visuals

class Schools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    num_of_students = db.Column(db.Integer)
    percent_bl = db.Column(db.Integer)
    percent_as = db.Column(db.Integer)
    percent_his = db.Column(db.Integer)
    percent_nat = db.Column(db.Integer)
    percent_paci = db.Column(db.Integer)
    percent_whit = db.Column(db.Integer)
    percent_two = db.Column(db.Integer)
    percent_low = db.Column(db.Integer)

    def __repr__(self):
        return '<School %s, %s - %s - %s%% - %s%% - %s%%>' % (
                self.name, self.city, 
                self.num_of_students, self.percent_bl, 
                self.percent_as, self.percent_his
            )

@app.route('/',  methods=['POST', 'GET'])
def index():
    schools = Schools.query.order_by(Schools.num_of_students.desc()).all()
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
                    .all()
                )
        else:
            schools = (
                    Schools.query.filter(filter_ > filter_percent)
                    .order_by(Schools.num_of_students.desc())
                    .all()
                )
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

if __name__ == "__main__":
    app.run(debug=True)