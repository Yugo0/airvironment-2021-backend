from app import db
from sqlalchemy import func


class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    pollution = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, temperature, humidity, pollution):
        self.temperature = temperature
        self.humidity = humidity
        self.pollution = pollution


    def __repr__(self):
        return f"Temperature: {self.temperature}\n"\
               f"Humidity: {self.humidity}\n"\
               f"Pollution: {self.pollution}\n" \
               f"Created: {self.created}\n"
