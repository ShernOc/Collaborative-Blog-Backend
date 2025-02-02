import flask
from flask import jsonify,request, Blueprint
from models import db, User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 
user_bp = Blueprint("user_bp", __name__)

#get all users
@user_bp.route('/users', methods = ['GET'])
def get_all_users():
    # get all the users 
    users = User.query.all()
    #create an empty list to store the users 
    user_list= []
    
    for user in users:
        user_list.append({  "id": user.id,
        "name":user.name,
        "email":user.email,
        "password": user.password,
        # "is_admin":user.is_admin,   
        })
    return jsonify({"All Users":user_list})

# Get users by id 
@user_bp.route('/users/<int:user_id>', methods = ['GET'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({  
        "id":user.id,
        "name":user.name,
        "email":user.email,
        "password": user.password,
        # "is_admin":user.is_admin,
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
    
#Create /post a User 
@user_bp.route('/users', methods = ["POST"])
def post_user_id():
    
    data = request.get_json(force=True, silent=True)
    
    print("Receiving data:", data)
    
    if not data: 
        return jsonify({"Error": "Invalid request "})
    
    required_fields = ["name", "email", "password"]
    
    missing_fields = [field for field in required_fields if field not in data]
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    # is_admin = bool(data.get("is_admin", False))

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    
    name = data["name"]
    email = data["email"]
    password =generate_password_hash(data["password"])
    # is_admin=data["is_admin"]
    
    #Check name or email of the user exist and if error message. 
    check_name = User.query.filter_by(name=name).first()
    check_email = User.query.filter_by(email=email).first()
    
    if check_name or check_email:
        return jsonify({"Error": "The User already added"}), 406
    else: 
        #create a new user 
        new_user = User(name=name,email=email,password=password)
        
        #call the function 
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": "User added successfully"}), 201
    
#Update a User  
@user_bp.route('/users/update', methods = ["PATCH","PUT"])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    # user will be none if no user is found
    # get all the Users 
    user= User.query.get(current_user_id)
    
    # check if not the current_user
    if not user:
        return jsonify({"Error":"Login to Update/ User not Found"}), 404
    
 #if the data is not provided issues the data
    data = request.get_json()
    name = data.get("name", user.name)
    email = data.get("email", user.email)
    password = data.get("password", user.password)
    # is_admin= data.get("is_admin", user.is_admin)    
    
    
    # user= User.query.get(current_user_id)
    # check if the name already exist in the database 
    check_name = User.query.filter_by(name=name and id!=user).first()
    check_email= User.query.filter_by(email=email and id!=user).first()
        
    #if the user with name or email exist 
    if check_name and check_email:
        return jsonify({"Error": "Name or Email already exist. Update a different name or email or something else"}),406
    
    #check if the data is the identical to the current_user/ and nothing has been changed.
    if name==user.name and email==user.email:
        return jsonify({"Error":"No change detected in your update"}), 400
    
    else: 
        #if no conflict update data
            user.name = name 
            user.email = email
            # user.is_admin = is_admin
            if password:
                user.password = generate_password_hash(password)
        
            #commit the function 
            db.session.commit()
            return jsonify({"Success": f"User with  ID {current_user_id} was updated successfully"}),200
        

#User Can Delete there own Accounts
@user_bp.route('/users/delete' ,methods=['DELETE']) 
@jwt_required()
def delete_user():
    #get the all the users
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "Delete your own account/ User not found "})
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"Success":"User deleted Successfully"})
    else:
         return jsonify({"Error": "User does not exist"}), 406
     

# Deleting all users can be done by the admin only 
@user_bp.route('/users/<int:user_id>/delete', methods=['DELETE']) 
@jwt_required()      
def delete_all_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id) # get the admin id. 
    # get the all the user
    if not current_user :
        return jsonify({"Error": "You are not an admin to delete an account "}), 403 
    
    user_delete= User.query.get(user_id)
    if not user_delete: 
        return jsonify({"Error": "User not Found"})
    #if the user is the admin then no deletion can happen
    if user_delete.id == current_user.id:
        return jsonify({"Error": "You cannot delete your own account"})
    else: 
        db.session.delete(user_delete)
        db.session.commit()
        return jsonify({"Success":f"User with {user_id}  has been deleted successfully"}), 200
    