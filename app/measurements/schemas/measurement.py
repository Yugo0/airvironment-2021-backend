from marshmallow import Schema, fields, validates, ValidationError, pre_load
from app.measurements.constants import PAGE, PER_PAGE


class MeasurementResponseSchema(Schema):
    id = fields.Integer(required=False)
    temperature = fields.Float()
    pollution = fields.Float()
    humidity = fields.Float()
    created = fields.DateTime()


class MeasurementRequestSchema(Schema):
    temperature = fields.Float(required=True)
    pollution = fields.Float(required=True)
    humidity = fields.Float(required=True)

    @validates("temperature")
    def validate_temperature(self, value):
        if value < -100 or value > 100:
            raise ValidationError("Temperature out of bounds")

    @validates("pollution")
    def validate_pollution(self, value):
        if value < 0:
            raise ValidationError("Pollution out of bounds")

    @validates("humidity")
    def validate_humidity(self, value):
        if value < 0 or value > 100:
            raise ValidationError("Humidity out of bounds")


class MeasurementPatchSchema(Schema):
    temperature = fields.Float(required=False)
    pollution = fields.Float(required=False)
    humidity = fields.Float(required=False)

    @validates("temperature")
    def validate_temperature(self, value):
        if value < -100 or value > 100:
            raise ValidationError("Temperature out of bounds")

    @validates("pollution")
    def validate_pollution(self, value):
        if value < 0:
            raise ValidationError("Pollution out of bounds")

    @validates("humidity")
    def validate_humidity(self, value):
        if value < 0 or value > 100:
            raise ValidationError("Humidity out of bounds")

    @pre_load()
    def something(self, data, **kwargs):
        if "temperature" not in data and "humidity" not in data and "pollution" not in data:
            raise ValidationError("Nothing to patch")
        return data


class MeasurementMetaSchema(Schema):
    page = fields.Integer(required=False, default=PAGE, missing=PAGE)
    per_page = fields.Integer(required=False, default=PER_PAGE, missing=PER_PAGE)
    total = fields.Integer(required=False, default=0, missing=0)


class MeasurementPaginationSchema(Schema):
    meta = fields.Method("get_meta")
    items = fields.List(fields.Nested(MeasurementResponseSchema()), data_key="response")

    @staticmethod
    def get_meta(data):
        return MeasurementMetaSchema().dump(data)
