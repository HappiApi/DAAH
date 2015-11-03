from flask import Flask, render_template
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def hello():
    return render_template('login.html', title="LOGIN")

@app.route("/lists")
def temp():
    return render_template('lists.html', title="Lists")

@app.route("/listname")
def temp1():
    return render_template('items.html', title="listname")


if __name__ == "__main__":
    app.run()
