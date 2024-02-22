import os
from flask import Flask, render_template, request


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.root_path, 'work_days.sqlite')
)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print(request.form['username'], request.form['password'])
    return render_template("auth/register.html")

@app.route("/auth/login", methods=['POST', 'GET'])
def login():
    return render_template("auth/login.html")

from . import db
with app.app_context():
        db.init_db()
        
from . import auth
app.register_blueprint(auth.bp)