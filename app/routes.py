from app import app
from flask import render_template
from app import db
from app.model import Measurement


@app.route("/")
def hello_world():
    objects = db.session.query(Measurement).all()
    return render_template("base.html", lista=objects)
