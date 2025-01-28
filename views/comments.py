from flask import jsonify,request, Blueprint
from models import db, Comment
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 

comment_bp = Blueprint("comment_bp", __name__)