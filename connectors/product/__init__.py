from flask import Blueprint

product = Blueprint("product", __name__)

from . import product_routes