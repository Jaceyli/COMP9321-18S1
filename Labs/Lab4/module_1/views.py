import datetime

from flask import Flask, session, request, redirect, url_for, render_template, make_response, Blueprint
from module_1.models import Teacher, Student
from module_1.serialize import deserialize, serialize

mod = Blueprint('module_1', __name__, url_prefix='')


@mod.route('/', methods=["GET"])
def index():
    teacher = retrieve_teacher()
    if teacher is None:
        # print("--------------------session is None")
        return redirect(url_for(".register"))
    return redirect(url_for(".show_students"))


@mod.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("module_1/register.html")
    else:
        name = request.form.get("name")
        course = request.form.get("course")
        teacher = Teacher(name, course)

        session["teacher"] = serialize(teacher)
        return redirect(url_for(".index"))


@mod.route('/student', methods=["GET"])
def show_students():
    teacher = retrieve_teacher()
    if teacher is None:
        return redirect(url_for(".register"))
    else:
        return render_template("module_1/students.html", students=teacher.students.values())


@mod.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return  render_template("module_1/add.html")
    else:
        id = request.form.get("id")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        gender = request.form.get("gender")
        teacher = retrieve_teacher()
        teacher.students[id] = Student(id, firstname, lastname, gender)
        session['teacher'] = serialize(teacher)
        return redirect(url_for(".show_students"))


@mod.route('/delete/<id>', methods=["POST", "GET", "DELETE"])
def delete(id):
    teacher = retrieve_teacher()
    teacher.students.pop(id)
    session["teacher"] = serialize(teacher)
    return redirect(url_for(".show_students"))


@mod.route('/edit/<id>', methods=["POST", "GET"])
def edit(id):
    teacher = retrieve_teacher()
    student = teacher.students.pop(id)
    if request.method == "GET":
        return render_template("module_1/edit.html", student=student)
    else:
        student.first_name = request.form.get("firstname")
        student.last_name = request.form.get("lastname")
        student.gender = request.form.get("gender")

        teacher.students[id] = student
        session["teacher"] = serialize(teacher)
        return redirect(url_for(".show_students"))


'''
The function stores the information of a teacher into a cookie
'''
@mod.route('/save')
def save():
    serialized_teacher = session.get("teacher")
    resp = make_response(render_template("module_1/save.html"))
    if serialized_teacher is not None:
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        resp.set_cookie("_teacher", serialized_teacher, expires=expire_date)

    return resp


'''
checks whether or not a teacher object exists in the session.
If not, the function shows the register page
'''
def retrieve_teacher():
    serialized_teacher = session.get("teacher")
    if serialized_teacher is None:
        serialized_teacher = request.cookies.get('teacher')
    if serialized_teacher is not None:
        # print('got session')
        return deserialize(serialized_teacher)
    return None
