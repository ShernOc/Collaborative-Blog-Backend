from flask import jsonify,request, Blueprint
from models import db, Blog
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 

blog_bp = Blueprint("blog_bp", __name__)