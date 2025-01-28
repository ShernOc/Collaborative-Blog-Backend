from flask import jsonify,request,Blueprint
from models import db,User,TokenBlocklist
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

# blueprint
auth_bp= Blueprint('auth_bp', __name__)