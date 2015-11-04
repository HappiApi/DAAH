from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

def check_login():
    if not session.get('user_id'):
        return redirect(url_for('/'))

def list_belongs_to_user(list_id):
    list = List.query.filter_by(id = list_id).first()
    return session.get('user_id') == list.user_id

def task_belongs_to_list(list_id, task_id):
    item = Task.query.filter_by(id = task_id).first()
    return list_id == item.list_id

@app.route("/")
def login():
    if not session.get('user_id'):
        return render_template('login.html', title="Login")
    return redirect(url_for('/lists'))

#CODE FOR LISTS

@app.route("/lists", methods=['GET'])
def show_lists():
    check_login()
    lists = List.query.filter_by(user_id=session.get('user_id'))
    return render_template('lists.html', title="Lists", lists=lists)

@app.route('/lists', methods=['POST'])
def new_list():
    check_login()
    list = List(request.form['name'], session.get('user_id'))
    db.session.add(list)
    db.session.commit()

    lists = List.query.filter_by(user_id=session.get('user_id'))
    return render_template('lists.html', title='Lists', lists=lists, message="Successfully created list")


@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list():
    check_login()
    if list_belongs_to_user(request.form[list_id]):
        list = List.query.filter_by(id = list_id).first()
        db.session.delete(list)
        db.session.commit()
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='Deleted List')
    else:
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='An error occured')

@app.route("/lists/<list_id>", methods=['POST'])
def edit_list():
    check_login()
    if list_belongs_to_user(list_id):
        list = Lists.query.filter_by(id = list_id).first()
        list.name = request.form['list_name']
        db.session.commit()
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='Successfully edited list')
    else:
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='An error occured')

#Displays tasks in list
@app.route("lists/<list_id>", methods=['GET'])
def show_list():
    check_login()
    if list_belongs_to_user(list_id):
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', items=tasks)
    else:
        return redirect(url_for('/lists'))

@app.route("list/<list_id>/task/<task_id>", methods=['POST']):
def delete_item():
    check_login()
    if list_belongs_to_user(list_id) && task_belongs_to_list(list_id, task_id):
        task = Task.query.filter_by(id = task_id).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', items=tasks, message='Successfully delete task')
    else:
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', items=tasks, message='An error occured')

@app.route("list/<list_id>/task/<task_id>", methods=['POST']):
def edit_item():
    check_login()
    if list_belongs_to_user(list_id) && task_belongs_to_list(list_id, task_id):
        task = Task.query.filter_by(id = task_id).first()
        task.name = request.form['list_name']
        db.session.commit()
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', items=tasks, message='Successfully edited task')
    else:
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', items=tasks, message='An error occured')


if __name__ == "__main__":
    app.run()
