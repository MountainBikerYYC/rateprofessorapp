from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/prof_review'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = "In ENV"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    professor =db.Column(db.String(200))
    department =db.Column(db.String(200))
    rating =db.Column(db.Integer)
    comments =db.Column(db.Text())

    def __init__(self, professor, department, rating, comments):
        self.professor = professor
        self.department = department
        self.rating = rating
        self.comments = comments

@app.route('/', methods=['GET','POST'])
def index():
    if request.method =='POST':
        if request.form.get("button3"):
             return redirect(url_for('tables'), code=302, Response=None)
    return render_template('index.html')

@app.route('/base', methods=['GET','POST'])
def base():
    if request.method =='POST':
        if request.form.get("button1"):
            return redirect(url_for('index'), code=302, Response=None)

@app.route('/server_table', methods=['GET','POST'])
def tables():
    result = Feedback.query.all()
    unique = db.engine.execute("SELECT DISTINCT professor, ROUND(AVG(rating),1) as rating, department, COUNT(professor) as count FROM public.feedback GROUP BY professor, department ORDER BY rating DESC")

    return render_template('server_table.html',title='All Professors', result=result, unique=unique)

@app.route('/success', methods=['GET','POST'])
def success():
    if request.form.get("button1"):
            return redirect(url_for('index'), code=302, Response=None)
        
    if request.form.get("button2"):
             return redirect(url_for('tables'), code=302, Response=None)
    return render_template('success.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        professor = request.form['professor']
        department = request.form['department']
        rating = request.form['rating']
        comments = request.form['comments']
    
        if professor == '' or department == '':
            return render_template('index.html', message='Please enter required fields')

        data = Feedback(professor, department, rating, comments)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('success'), code=302, Response=None)


if __name__ == '__main__':
    app.debug = True
    app.run()