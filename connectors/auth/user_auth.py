from . import auth
from flask import Flask, request, jsonify, Blueprint
from models.users import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not fullname or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    try:
        new_user = User(username=username, fullname=fullname, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error registering user"}), 500


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "user_id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "image_url": user.image_url
        }), 200
