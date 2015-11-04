from flask import Flask, render_template
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def hello():
    return render_template('login.html', title="Log In")

@app.route("/signup")
def signup():
    return render_template('signup.html', title="Sign Up")

@app.route("/lists")
def lists():
    return render_template('lists.html', title="Lists")

@app.route("/newlist")
def newlist():
    return render_template('newlist.html', title="New List")

@app.route("/newitem")
def newitem():
    return render_template('newitem.html', title="New Item")

if __name__ == "__main__":
    app.run()
