from app import db
from app.measurements import measurement_bp
from app.measurements.model import Measurement
from flask import request
from werkzeug.exceptions import NotFound
from app.measurements.schemas import MeasurementResponseSchema, MeasurementRequestSchema, MeasurementPatchSchema, \
    MeasurementMetaSchema, MeasurementPaginationSchema

measurement_response_schema = MeasurementResponseSchema()
measurement_collection_response_schema = MeasurementResponseSchema(many=True)
measurement_meta_schema = MeasurementMetaSchema()
measurement_pagination_schema = MeasurementPaginationSchema()


@measurement_bp.get('')
def get_all():
    schema_load = measurement_meta_schema.load(request.args.to_dict())

    measurements = db.session.query(Measurement).paginate(page=schema_load.get("page"),
                                                          per_page=schema_load.get("par_page"))

    # response = {"meta": {"total": measurements.total,
    #                      "page": measurements.page,
    #                      "per_page": measurements.per_page},
    #             "results": []}
    #
    # for measurement in measurements.items:
    #     data = {"id": measurement.id,
    #             "temperature": measurement.temperature,
    #             "pollution": measurement.pollution,
    #             "humidity": measurement.humidity}
    #     response['results'].append(data)
    # return json.dumps(response)
    return measurement_pagination_schema.dump(measurements)


@measurement_bp.get('/<int:id>')
def get_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(f"Measurement with id {id} not found")

    return measurement_response_schema.dump(measurement)


@measurement_bp.get('/latest')
def get_latest():
    measurement = db.session.query(Measurement).order_by(Measurement.created.desc()).first()

    if not measurement:
        return NotFound("Table empty")

    return measurement_response_schema.dump(measurement)


@measurement_bp.post('')
def post():
    measurement_request = MeasurementRequestSchema()

    data = measurement_request.load(request.json)

    measurement = Measurement(data.get("temperature"), data.get("humidity"), data.get("pollution"))

    db.session.add(measurement)
    db.session.commit()

    return measurement_response_schema.dump(measurement)


@measurement_bp.patch('/<int:id>')
def patch_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(f"Measurement with id {id} not found")

    measurement_patch = MeasurementPatchSchema()

    data = measurement_patch.load(request.json)

    temp = data.get("temperature")
    if temp:
        measurement.temperature = temp

    humid = data.get("humidity")
    if humid:
        measurement.humidity = humid

    poll = data.get("pollution")
    if poll:
        measurement.pollution = poll

    db.session.commit()

    return measurement_response_schema.dump(measurement)
