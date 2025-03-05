from . import transaction
from flask import Flask, request, jsonify, Blueprint
from models.users import db, User
from models.transactions import db, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

#test route
@transaction.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, Transaction!'}), 200

@transaction.route("/create", methods=["POST"])
def create_transaction():
    try:
        data = request.json
        user_id = data.get("user_id")
        departure = data.get("departure")
        destination = data.get("destination")
        bus_class = data.get("bus_class")
        date = data.get("date")
        selected_seats = data.get("selected_seats")
        total_price = data.get("total_price")

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_transaction = Transaction(
            user_id=user_id,
            departure=departure,
            destination=destination,
            bus_class=bus_class,
            date=date,
            selected_seats=selected_seats,
            total_price=total_price,
            status="confirmed",
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({"message": "Transaction created successfully", "transaction": new_transaction.to_dict()}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction.route("/user/<int:user_id>", methods=["GET"])
def get_transactions_by_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify({"transactions": [t.to_dict() for t in transactions]}), 200

@transaction.route("/update/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        data = request.json
        transaction.departure = data.get("departure", transaction.departure)
        transaction.destination = data.get("destination", transaction.destination)
        transaction.bus_class = data.get("bus_class", transaction.bus_class)
        transaction.date = data.get("date", transaction.date)
        transaction.selected_seats = data.get("selected_seats", transaction.selected_seats)
        transaction.total_price = data.get("total_price", transaction.total_price)
        transaction.status = data.get("status", transaction.status)

        db.session.commit()
        return jsonify({"message": "Transaction updated successfully", "transaction": transaction.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaction.route("/delete/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500