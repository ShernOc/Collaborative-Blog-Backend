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
    #get all the users 
    users = User.query.all()
    
    # users = User.query.filter_by(user_id = current_user_id)
    #create an empty list to store the users 
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
    user = User.query.get(id ==id)
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
    
    #Check name or email of the user exist and if error message. 
    check_name = User.query.filter_by(name=name).first()
    check_email = User.query.filter_by(email=email).first()
    
    if check_name or check_email:
        return jsonify({"Error": "The User Already exist"}), 406
    else: 
        #create a new user 
        new_user = User(name=name,email=email,password=password,is_admin=is_admin)
        
        #call the function 
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"Success": "User added Successfully"}), 201
    
    
#Update a User  
@user_bp.route('/users/<user_id>', methods = ["PATCH","PUT"])
def update_user_id(user_id):
    # user will be none if no user is found
    # get all the Users 
    user= User.query.get(user_id)
    
    # check if the user exist, 
    if user:
          #if the data is not provided issues the data
        data = request.get_json()
        name = data.get("name", user.name)
        email = data.get("email", user.email)
        password = data.get("password", user.password)
        is_admin= data.get("is_admin", user.is_admin)
        
    
    # check for existing name or email if they already exist
        check_name = User.query.filter_by(name=name and id!=user_id).first()
        check_email = User.query.filter_by(email=email and id!=user_id).first()
    
    #if the user with name or email exist 
        if check_name or check_email:
            return jsonify({"Error": "A user with this name or email already exist. Use a different name or email"}),406
        else: 
          #if no conflict update 
            user.name = name 
            user.email = email
            user.password = password
            user.is_admin = is_admin
        
            #commit the function 
            db.session.commit()
            return jsonify({"Success": f"User with {user_id} was updated successfully"}),200
    else:
        return jsonify({"Error": "The name or email of User not found. Kindly Create a User "}), 406
    
    
#Delete User 
@user_bp.route('/users/<int:user_id>' ,methods=['DELETE'])        
def delete_user(user_id):
    #get the all the users
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"Success":"User deleted Successfully"})
    else:
         return jsonify({"Error": "User does not exist"}), 406
      
        
    