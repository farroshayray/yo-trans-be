from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db
from connectors.auth import auth as auth_blueprint
from connectors.product import product as product_blueprint
from connectors.transaction import transaction as transaction_blueprint
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, unset_jwt_cookies
import os

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Register blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(product_blueprint, url_prefix='/product')
app.register_blueprint(transaction_blueprint, url_prefix='/transaction')

# JWT handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    response = jsonify({"msg": "Token has expired"})
    unset_jwt_cookies(response)
    return response, 401

@jwt.unauthorized_loader
def missing_jwt_callback(error):
    return jsonify({"msg": "Unauthorized, please login first"}), 401

@app.route('/')
def index():
    return '<div>Hello</div>'

if __name__ == '__main__':
    app.run(debug=app.config.get("DEBUG", False))
