import os
from forms import AddForm, DelForm, AddFaculty, AddEnrolled, AddClass
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = "knowledgeshelf"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app,db)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    major = db.Column(db.Text)
    level = db.Column(db.Text)
    age = db.Column(db.Integer,primary_key=True)

    def __init__(self,id,name,major,level,age):
        self.id = id
        self.name = name
        self.major = major
        self.level = level
        self.age = age


class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    dept_id = db.Column(db.Integer,primary_key=True)


    def __init__(self,id, name, dept_id):
        self.id = id
        self.name = name
        self.dept_id = dept_id


class Enrolled(db.Model):
    __tablename__ = 'enrolled'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    def __init__(self,id, name):
        self.id = id
        self.name = name


class CCLASS(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    meet_at = db.Column(db.Text)
    room = db.Column(db.Text)

    def __init__(self,name,id,meet_at,room):
        self.name = name
        self.id = id
        self.meet_at = meet_at
        self.room = room

   

# HOME
@app.route('/')
def index():
    return render_template('home.html')

# ADD A STUDENT
@app.route('/add',methods=['GET','POST'])
def add_student():

    form = AddForm()

    if form.validate_on_submit():

        id = form.id.data
        name = form.name.data
        major = form.major.data
        level = form.level.data
        age = form.age.data

        new_student = Student(id,name,major,level,age)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('list_student'))

    return render_template('add.html', form=form)

#ENROLLED
@app.route('/add_enrolled',methods=['GET','POST'])
def add_enrolled():

    form = AddEnrolled()

    if form.validate_on_submit():

        name = form.name.data
        id = form.id.data

        new_enrolled = Enrolled(name,id)
        db.session.add(new_enrolled)
        db.session.commit()
        return redirect(url_for('list_enrolled'))

    return render_template('add_enrolled.html', form=form)


#ADD FACULTY
@app.route('/add_faculty',methods=['GET','POST'])
def add_faculty():

    form = AddFaculty()

    if form.validate_on_submit():

        name = form.name.data
        id = form.id.data
        dept_id = form.dept_id.data

        new_faculty = Faculty(name,id,dept_id)
        db.session.add(new_faculty)
        db.session.commit()
        return redirect(url_for('list_faculty'))

    return render_template('add_faculty.html', form=form)


# CLASS
@app.route('/add_class',methods=['GET','POST'])
def add_class():

    form = AddClass()

    if form.validate_on_submit():

        name = form.name.data
        meet_at = form.meet_at.data
        room = form.room.data
        id = form.id.data

        new_class = CCLASS(name,id,meet_at,room)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('list_class'))

    return render_template('add_class.html', form=form)



# LIST OF STUDENTS
@app.route('/list')
def list_student():

    students = Student.query.all()
    return render_template('list.html', students=students)

# LIST OF FACULTY
@app.route('/list_faculty')
def list_faculty():

    faculty = Faculty.query.all()
    return render_template('list_faculty.html', faculty=faculty)

# LIST OF Enrolled
@app.route('/list_enrolled')
def list_enrolled():

    enrolled = Enrolled.query.all()
    return render_template('list_enrolled.html', enrolled=enrolled)

# LIST OF CLASS
@app.route('/list_class')
def list_class():

    cclass = CCLASS.query.all()
    return render_template('list_enrolled.html', cclass=cclass)


# DELETE A DATA
@app.route('/delete',methods=['GET','POST'])
def del_student():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('list_student'))

    return render_template('delete.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)