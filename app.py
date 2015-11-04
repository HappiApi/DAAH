from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import User

@app.route("/")
def hello():
    return render_template('login.html', title="LOGIN")

if __name__ == "__main__":
    app.run()
