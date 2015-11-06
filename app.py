from flask import Flask, render_template, request, redirect, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask import session
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
app.config.from_object(__name__)

from models import *

def list_belongs_to_user(list_id):
    try:
        list = List.query.filter_by(id = list_id).first()
        return session.get('user_id') == list.user_id
    except:
        return False

def task_belongs_to_list(list_id, task_id):
    item = Task.query.filter_by(id = task_id).first()
    print("ITEM = " +  str(item.list_id))
    return list_id == item.list_id

#LOGGING IN

@app.route("/", methods=['GET'])
def hello():
    if not session.get('user_id'):
        return render_template('login.html', title="Login")
    return redirect('/lists')

@app.route("/", methods=['POST'])
def login():
    if not request.form['username'] or not request.form['password']:
        return render_template('login.html', title="Login", message='Fields cannot be empty')
    else:
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            return render_template('login.html', title="Login", message='User not found')
        if  user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect('/lists')
    return render_template('login.html', title="Login", message='Something went wrong')

#SIGNING UP

@app.route('/signup', methods=['GET'])
def signup():
    if not session.get('user_id'):
        return render_template('signup.html', title="Signup")
    return redirect('/lists')


@app.route('/signup', methods=['POST'])
def new_user():
    if not request.form['username'] or not request.form['password1'] or not request.form['password2']:
        return render_template('signup.html', title="Signup", message='Fields cannot be empty')
    if not (request.form['password1'] == request.form['password2']):
        return render_template('signup.html', title="Signup", message='Passwords do not match')
    try:
        user = User()
        user.username = request.form['username']
        user.set_password(request.form['password1'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
    except:
        return render_template('signup.html', title="Signup", message='User already exists')

    return redirect('/lists')

#LOGGING OUT
@app.route('/logout')
def logout():
    if not session.get('user_id'):
      return redirect('/')
    session.pop('user_id', None)
    return redirect('/')

#CODE FOR LISTS

@app.route("/lists", methods=['GET'])
def show_lists():
    if not session.get('user_id'):
        return redirect('/')
    lists = List.query.filter_by(user_id=session.get('user_id'))
    if not lists:
        render_template('lists.html', title='Lists', message='No lists here...')
    return render_template('lists.html', title="Lists", lists=lists)

@app.route('/lists', methods=['POST'])
def new_list():
    if not session.get('user_id'):
      return redirect('/')
    name = request.form['name']
    if not name or name == "":
        return render_template('newlist.html', title='New List', message="Something went wrong")
    list = List(request.form['name'], session.get('user_id'))
    db.session.add(list)
    db.session.commit()

    lists = List.query.filter_by(user_id=session.get('user_id'))
    return render_template('lists.html', title='Lists', lists=lists, message="Successfully created list")

@app.route('/newlist')
def display_new_list():
    if not session.get('user_id'):
        return redirect('/')
    return render_template('newlist.html', title='New List')

@app.route('/editlist/<list_id>')
def display_edit_list(list_id):
    if not session.get('user_id'):
        return redirect('/')
    if list_belongs_to_user(list_id):
        list = List.query.filter_by(id = list_id).first()
        return render_template('newlist.html', title='Edit list', list_name=list.name, list_id = list_id)
    return redirect('/lists')

@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        list = List.query.filter_by(id = list_id).first()
        db.session.delete(list)
        db.session.commit()
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='Deleted List')
    else:
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='An error occured')

@app.route("/lists/<list_id>", methods=['POST'])
def edit_list(list_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        list = List.query.filter_by(id = list_id).first()
        list.name = request.form['name']
        db.session.commit()
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='Successfully edited list')
    else:
        lists = List.query.filter_by(user_id=session.get('user_id'))
        return render_template('lists.html', title='Lists', lists=lists, message='An error occured')

#TASKS

@app.route("/lists/<list_id>/newtask", methods=['GET'])
def show_new_task(list_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        list = List.query.filter_by(id=list_id).first()
        return render_template('newitem.html', title='New Task', list=list)
    else:
        list = List.query.filter_by(id=list_id).first()
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', tasks=tasks, list=list, message='An error occured')
#Displays tasks in list
@app.route("/lists/<list_id>", methods=['GET'])
def show_list(list_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        list = List.query.filter_by(id=list_id).first()
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', list=list, items=tasks)
    else:
        return redirect('/lists')

@app.route("/lists/<list_id>/tasks/<task_id>", methods=['DELETE'])
def delete_item(list_id, task_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        task = Task.query.filter_by(id = task_id).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.filter_by(list_id=list_id)
        list = List.query.filter_by(id=list_id).first()
        return render_template('items.html', title='Tasks', list=list, items=tasks, message='Successfully delete task')
    else:
        list = List.query.filter_by(id=list_id).first()
        tasks = Task.query.filter_by(list_id=list_id)
        return render_template('items.html', title='Tasks', list=list, items=tasks, message='An error occured')

@app.route("/lists/<list_id>/tasks/<task_id>", methods=['POST'])
def edit_item(list_id, task_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        task = Task.query.filter_by(id = task_id).first()
        task.name = request.form['name']
        db.session.commit()
        tasks = Task.query.filter_by(list_id=list_id)
        list = List.query.filter_by(id=list_id).first()
        return render_template('items.html', title='Tasks', list = list, items=tasks, message='Successfully edited task')
    else:
        tasks = Task.query.filter_by(list_id=list_id)
        list = List.query.filter_by(id=list_id).first()
        return render_template('items.html', title='Tasks', list=list,items=tasks, message='An error occured')

@app.route("/lists/<list_id>/newtask", methods=['POST'])
def new_item(list_id):
    if not session.get('user_id'):
      return redirect('/')
    if list_belongs_to_user(list_id):
        task = Task(request.form['name'], list_id)
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.filter_by(list_id=list_id)
        list = List.query.filter_by(id=list_id).first()
        return render_template('items.html', title='Tasks', list=list, items=tasks, message='Added task')
    tasks = Task.query.filter_by(list_id=list_id)
    list = List.query.filter_by(id=list_id).first()
    return render_template('items.html', title='Tasks', list=list, items=tasks, message='An error occured')

@app.route("/lists/<list_id>/tasks/<task_id>/edit", methods=['GET'])
def show_edit_item(list_id, task_id):
    if not session.get('user_id'):
      return redirect('/')
    print(list_belongs_to_user(list_id))
    print(task_belongs_to_list(list_id, task_id))
    if list_belongs_to_user(list_id):
        list = List.query.filter_by(id=list_id).first()
        task = Task.query.filter_by(id=task_id).first()
        return render_template('newitem.html', title="Edit Task", list=list, task=task)
    list = List.query.filter_by(id=list_id).first()
    return redirect('/lists/' + str(list.id))

if __name__ == "__main__":
    app.secret_key="SUPER SECRET, SHHHHHH!!"
    app.run()
