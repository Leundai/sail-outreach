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
    type_of = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    num_of_students = db.Column(db.Integer)
    percent_af = db.Column(db.Integer)
    percent_as = db.Column(db.Integer)
    percent_his = db.Column(db.Integer)
    percent_ind = db.Column(db.Integer)
    percent_paci = db.Column(db.Integer)
    percent_whit = db.Column(db.Integer)
    percent_two = db.Column(db.Integer)
    percent_unsp = db.Column(db.Integer)
    percent_free = db.Column(db.Integer)

    def __repr__(self):
        return '<School %s %s %s %s %s %s %s>' % (self.name, self.city, self.type_of, self.num_of_students, self.percent_af, self.percent_as, self.percent_his)

@app.route('/',  methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)