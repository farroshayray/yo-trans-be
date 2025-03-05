from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal

class BusClass(db.Model):
    __tablename__ = "bus_classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nama kelas bus (Executive, Business)
    description = db.Column(db.Text, nullable=True)  # Deskripsi opsional
    seats = db.relationship("Seat", backref="bus_class", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BusClass {self.name}>"


class Seat(db.Model):
    __tablename__ = "seats"

    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(10), nullable=False)  # Nomor kursi (A1, B2, dsb.)
    seat_type = db.Column(db.String(50), nullable=False)  # Jenis kursi (Sleeper, Regular, dll.)
    price = db.Column(db.Float, nullable=False)  # Harga kursi
    bus_class_id = db.Column(db.Integer, db.ForeignKey("bus_classes.id"), nullable=False)  # Relasi ke BusClass

    def __repr__(self):
        return f"<Seat {self.seat_number} - {self.seat_type} (${self.price})>"
