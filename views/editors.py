from flask import jsonify,request, Blueprint
from models import db, Editors, Blog,User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 
editor_bp = Blueprint("editor_bp", __name__)

#fetch/get the editors
@editor_bp.route('/editors', methods = ['GET'])
@jwt_required()
def get_all_editors():
    current_user_id=get_jwt_identity()
    # get all editors
    editors = Editors.query.all()
    user = User.query.all(current_user_id)
    #create an empty list 
    editors_list = []
    if user or user.is_admin:
        for edit in editors:
                editors_list.append({
                    "id":edit.id,
                    "blog_id":edit.blog_id,
                    "user_id":edit.user_id,
                    "role":edit.role
            })
        return jsonify({"Editors": editors_list})

# Get editor by id by admin
@editor_bp.route('/editors/<int:editor_id>', methods = ['GET'])
@jwt_required()
def get_editors_id(editor_id):
    current_user_id = get_jwt_identity()
    #check if user is also an admin 
    user = User.query.all(current_user_id)
    
    editor = Editors. query.all()

    if not user or not user.is_admin:
        return jsonify({"Error": "Not authorized to access only admin"})
    
    #check if the editor exist 
    editor= Editors.query.get(editor_id)
    if not editor: 
        return jsonify({"Error": "Editor not found"}), 404 
    
    editor_blog = {  
        "id":editor.id,
        "blog_id":editor.blog_id,
        "user_id":editor.user_id,
        "role":editor.role,
        "blogs":[{"title":blog.title} for blog in editor_blog]
        }
        
    return jsonify({"Editor": editor_blog}), 200

    
#Post/create an editor / id admin 
@editor_bp.route('/editors/<int:blog_id>/<int:user_id>',methods =['POST'])
@jwt_required()
def assign_editor(blog_id,user_id):
    current_user_id=get_jwt_identity()
    #check if the blog exist
    blog = Blog.query.get(blog_id)
    
    if not blog:
        return jsonify({"Error":"Blog not found."}), 404
    
    users = User.query.get(current_user_id)
    
    if blog.user_id != current_user_id and not users.is_admin:
        return jsonify({"Error": " You are Unauthorized to assign editor role."}), 403
    
    already_editor = Editor.query.fitler_by(blog_id=blog_id, user_id=user_id).first()
    if already_editor: 
        return jsonify({"Error": "User is already an editor to a blog"})


    new_editor= Editors(blog_id = blog_id, user_id=current_user_id,  role="editor")
    db.session.add(new_editor)
    db.session.commit()
    return jsonify({"Success":"Editor added successfully"}), 201
    
    
#Update a editor based on the id
@editor_bp.route('/editors/<editor_id>', methods = ["PATCH","PUT"])
@jwt_required()
def update_editor_id(editor_id):
    current_user_id=get_jwt_identity()

    # get all the Editors/ users 
    users = User.query.get(current_user_id)
    editor= Editors.query.get(editor_id)
    
    if not editor:
        return jsonify({"Error": "Editor is not found"}), 404
    
    # check if the edit exist, 
    if editor != current_user_id and not users.is_admin :
        return jsonify({"Error": "Editor not found, authorized  to update "}),404
    
    #get the data to pass the new editor 
    data = request.get_json()
    blog_id= data.get("blog_id", editor.blog_id)
    user_id = data.get("user_id",editor.user_id)
    role = data.get("role",editor.role)
  
# check for existing blog_id or user_id if they already exist
    check_user= Editors.query.filter(Editors.user_id==user_id and Editors.id!=editor_id).first()
    check_blog =Editors.query.filter(Editors.blog_id == blog_id and Editors.id!=editor_id).first()

#if the editor with a  user or role exist 
    if check_user or check_blog:
        return jsonify({"Error": "The editor already exist with the blog_id and user_id "}),406
    else: 
    #if no conflict update 
        editor.blog_id = blog_id 
        editor.user_id = user_id
        editor.role = role

    # and commit the change 
        db.session.commit()
        return jsonify({"Success": f"Editor with id {editor_id} is updated successfully"}),200
    
    
#Delete Editor   
@editor_bp.route('/editors/<int:blog_id>/<int:user_id>' ,methods=['DELETE'])      
@jwt_required()
def delete_editors(user_id, blog_id):
    current_user_id=get_jwt_identity()

    # check if the blog exist 
    blog = Blog.query.get(blog_id)
    if not blog:
        return jsonify({"Error":"Blog not found."}), 404
    
    #check if user is admin 
    user = User.query.get(current_user_id)
    if blog.user_id !=current_user_id and not user.is_admin:
        return jsonify({"Error": "Not authorized to remove an editor role"}), 403
    
    remove_editor= Editors.query.filter_by(blog_id=blog_id, user_id =user_id).first()
    
    if not remove_editor:
        return jsonify({"Error": "Editor does not exist"})
    
    db.session.delete(remove_editor)
    db.session.commit()
    return jsonify({"Success":"Editor deleted successfully"})
  

# # Delete All editors
# @editor_bp.route('/editors', methods=['DELETE'])      
# def delete_all_editor():
#     #get the all the users
#     user = Editors.query.delete()
#     db.session.commit()
#     return jsonify({"Success":"Editors deleted successfully"})
        