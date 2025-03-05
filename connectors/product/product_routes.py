from . import product
from flask import Flask, request, jsonify, Blueprint
from models.users import db, User
from models.products import db, BusClass, Seat
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

#test endpoint
@product.route('/', methods=['GET'])
def get_products():
    return jsonify({'message': 'Hello, World!'})

@product.route("/bus-classes", methods=["POST"])
def create_bus_class():
    """Tambah kelas bus baru"""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"message": "Bus class name is required"}), 400

    new_bus_class = BusClass(name=name, description=description)
    db.session.add(new_bus_class)
    db.session.commit()
    return jsonify({"message": "Bus class added successfully", "bus_class": {"id": new_bus_class.id, "name": new_bus_class.name}}), 201


@product.route("/bus-classes", methods=["GET"])
def get_bus_classes():
    """Ambil semua kelas bus"""
    bus_classes = BusClass.query.all()
    result = [{"id": b.id, "name": b.name, "description": b.description} for b in bus_classes]
    return jsonify(result), 200


@product.route("/bus-classes/<int:id>", methods=["GET"])
def get_bus_class(id):
    """Ambil detail kelas bus + semua kursi yang tersedia"""
    bus_class = BusClass.query.get(id)
    if not bus_class:
        return jsonify({"message": "Bus class not found"}), 404

    seats = [{"id": s.id, "seat_number": s.seat_number, "seat_type": s.seat_type, "price": s.price} for s in bus_class.seats]
    
    return jsonify({
        "id": bus_class.id,
        "name": bus_class.name,
        "description": bus_class.description,
        "seats": seats
    }), 200


@product.route("/bus-classes/<int:id>", methods=["PUT"])
def update_bus_class(id):
    """Update kelas bus"""
    bus_class = BusClass.query.get(id)
    if not bus_class:
        return jsonify({"message": "Bus class not found"}), 404

    data = request.get_json()
    bus_class.name = data.get("name", bus_class.name)
    bus_class.description = data.get("description", bus_class.description)
    db.session.commit()
    
    return jsonify({"message": "Bus class updated successfully"}), 200


@product.route("/bus-classes/<int:id>", methods=["DELETE"])
def delete_bus_class(id):
    """Hapus kelas bus beserta semua kursinya"""
    bus_class = BusClass.query.get(id)
    if not bus_class:
        return jsonify({"message": "Bus class not found"}), 404

    db.session.delete(bus_class)
    db.session.commit()
    
    return jsonify({"message": "Bus class deleted successfully"}), 200


@product.route("/seats", methods=["POST"])
def create_seat():
    """Tambah kursi ke kelas bus tertentu"""
    data = request.get_json()
    seat_number = data.get("seat_number")
    seat_type = data.get("seat_type")
    price = data.get("price")
    bus_class_id = data.get("bus_class_id")

    if not all([seat_number, seat_type, price, bus_class_id]):
        return jsonify({"message": "All seat fields are required"}), 400

    new_seat = Seat(seat_number=seat_number, seat_type=seat_type, price=price, bus_class_id=bus_class_id)
    db.session.add(new_seat)
    db.session.commit()
    
    return jsonify({"message": "Seat added successfully"}), 201


@product.route("/seats/<int:bus_class_id>", methods=["GET"])
def get_seats(bus_class_id):
    """Ambil semua kursi berdasarkan kelas bus"""
    seats = Seat.query.filter_by(bus_class_id=bus_class_id).all()
    if not seats:
        return jsonify({"message": "No seats found"}), 404

    result = [{"id": s.id, "seat_number": s.seat_number, "seat_type": s.seat_type, "price": s.price} for s in seats]
    return jsonify(result), 200


@product.route("/seats/<int:id>", methods=["PUT"])
def update_seat(id):
    """Update kursi"""
    seat = Seat.query.get(id)
    if not seat:
        return jsonify({"message": "Seat not found"}), 404

    data = request.get_json()
    seat.seat_number = data.get("seat_number", seat.seat_number)
    seat.seat_type = data.get("seat_type", seat.seat_type)
    seat.price = data.get("price", seat.price)
    db.session.commit()
    
    return jsonify({"message": "Seat updated successfully"}), 200


@product.route("/seats/<int:id>", methods=["DELETE"])
def delete_seat(id):
    """Hapus kursi"""
    seat = Seat.query.get(id)
    if not seat:
        return jsonify({"message": "Seat not found"}), 404

    db.session.delete(seat)
    db.session.commit()
    
    return jsonify({"message": "Seat deleted successfully"}), 200