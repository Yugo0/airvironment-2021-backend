from app import app
from flask import render_template

asd = [{"temperatura": 40},
         {"temperatura": 20},
         {"temperatura": 36}]

@app.route("/")
def hello_world():
    return render_template("base.html",lista=asd)
