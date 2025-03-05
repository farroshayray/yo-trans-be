from . import db
from datetime import datetime
from decimal import Decimal

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    departure = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    bus_class = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    selected_seats = db.Column(db.JSON, nullable=False)  # List kursi dalam format JSON
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum("pending", "confirmed", "cancelled", name="status_enum"), default="confirmed")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relasi ke tabel User
    user = db.relationship("User", backref=db.backref("transactions", lazy=True))

    def to_dict(self):
        """Return a dictionary representation of the Transaction."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "departure": self.departure,
            "destination": self.destination,
            "bus_class": self.bus_class,
            "date": self.date.isoformat(),
            "selected_seats": self.selected_seats,
            "total_price": float(self.total_price),  # Convert Decimal ke float
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
