from app import db
from app.measurements import measurements_bp
from app.measurements.models import Measurement
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE
from werkzeug.exceptions import NotFound


@measurements_bp.get('')
def get_all():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 1))

    measurements = db.session.query(Measurement).paginate(page=PAGE, per_page=PER_PAGE)

    response = {"meta": {"total": measurements.total,
                         "page": measurements.page,
                         "per_page": measurements.per_page},
                "results": []}

    # measurements = db.session.query(Measurement).all()
    # list_of_measurements = []
    #
    for measurement in measurements.items:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
        response['results'].append(data)
    return json.dumps(response)

@measurements_bp.get('/<int:id>')
def get_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(f"Measurement with id {id} not found")

    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    return json.dumps(data)

@measurements_bp.get('/latest')
def get_latest():
    measurement = db.session.query(Measurement).order_by(Measurement.created.desc()).first()

    if not measurement:
        return NotFound("Table empty")

    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    return json.dumps(data)

@measurements_bp.post('')
def post():
    data_ = request.json

    measurement = Measurement(data_.get("temperature"), data_.get("humidity"), data_.get("pollution"))

    db.session.add(measurement)
    db.session.commit()

    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    return json.dumps(data)

@measurements_bp.patch('/<int:id>')
def patch_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(f"Measurement with id {id} not found")

    data_ = request.json

    temp = data_.get("temperature", None)
    if temp:
        measurement.temperature = temp

    humid = data_.get("humidity", None)
    if humid:
        measurement.humidity = humid

    poll = data_.get("pollution", None)
    if poll:
        measurement.pollution = poll

    db.session.commit()

    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    return json.dumps(data)
