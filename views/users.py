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
        })
    return jsonify({"All Users":user_list})

# Get users by id 
@user_bp.route('/users/<int:id>', methods = ['GET'])
# @jwt_required()
def get_user_id(id):
    # current_user_id = get_jwt_identity()
    user = User.query.get(id)
    
    # users = User.query.filter_by(user_id = current_user_id)
    if user:
        return jsonify({  
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "password": user.password,
        "is_admin":user.is_admin,
        #Provides the blogs of the users have created
          "blogs":[
                {
                    "id":blogs.id,
                    "title":blogs.title,
                    
                } for blogs in user.blogs
            ],
          
          "comments":[
                {
                    "id":comments.id,
                    "content":comments.content,
                } for comments in user.comments
            ]
           
        })
    else: 
        return jsonify({"Error": "User does not exist"})


#Create a User  
@user_bp.route('/users', methods = ["POST"])
def post_user_id():
    # get the data
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]
    is_admin= data["is_admin"]
    
    check_name = User.query.get(name)
    check_email = User.query.get(name)
    
    if check_name or check_email:
        return jsonify({"Error": "The User Already exist"})
    else: 
        new_user = User(name=name,email=email,password=password,is_admin=is_admin)
        
        #call the function 
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"Success": "User added Successfully"})
    
    
#Update a User  
@user_bp.route('/users/<user_id>', methods = ["PATCH"])
def update_user_id(id):
    user= User.query.get(id)
    
    if user and user.id:
        # get the data
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        is_admin= data.get("is_admin")
        
        check_name = User.query.get(name)
        check_email = User.query.get(name)
    
    if check_name or check_email:
        return jsonify({"Error": "The User Already exist"})
    else: 
        new_user = User(name=name,email=email,password=password,is_admin=is_admin)
        
        #call the function 
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"Success": "User added Successfully"})
    
    
#DELETE USER; 
@user_bp.route('/users/<int:user_id>',methods=['DELETE'])        
def delete_user(user_id):
    #get the users
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"Success":"User Deleted Successfully"})
    else:
         return jsonify({"Error": "User does not exist"})
      
        