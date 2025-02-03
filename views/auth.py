from flask import jsonify,request,Blueprint
from models import db,User,TokenBlocklist
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime,timezone

# blueprint
auth_bp= Blueprint('auth_bp', __name__)

#Login User 
@auth_bp.route('/login',methods=['POST'])
#get the data of user
def login():
    #None is the email, or password does not exist
    data = request.get_json()
    email=data.get("email",None )
    password=data.get("password",None)
    
    #check if the user with the email exist (if)
    user=User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password,password):
        access_token = create_access_token(identity=str(user.id))
        print("Generated Token:", access_token)  # Debugging Line
        return jsonify({"access_token":access_token}), 200
    # pass an error 
    else: 
        return jsonify({"Error":"Not Logged in "}), 404
        
#get the current user functions
@auth_bp.route('/current_user', methods = ['GET'])
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    print(current_user_id)
    #fetch the user
    user = User.query.get(current_user_id)
    #get the user data object 
    user_data = [{
                "id":user.id,
                "name":user.name,
                "email":user.email}]
    
    return jsonify( {"Current_user":user_data})
    

#Logout / Revoke 
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"Success" : "User has been logged out Successfully "})


