from flask import Flask, render_template
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def hello():
    return render_template('login.html', title="LOGIN")

if __name__ == "__main__":
    app.run()
