from flask import jsonify,request, Blueprint
from models import db, User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 
user_bp = Blueprint("user_bp", __name__)

@user_bp.route('/users', methods = ['GET'])
# @jwt_required()
def get_user():
    # current_user_id = get_jwt_identity()
    
    users = User.query.all()
    
    # users = User.query.filter_by(user_id = current_user_id)
    user_list= []
    
    for user in users:
        user_list.append({  "id": user.id,
        "name":user.name,
        "email":user.email,
        "password": user.password,
        "is_admin":user.is_admin,
        #Provides the blogs of the users have created
          "blogs":[
                {
                    "id":blogs.id,
                    "title":blogs.title,
                    "content":blogs.content,
    
                } for blogs in user.blogs
            ] 
        })
    return jsonify(user_list)


    
      
        