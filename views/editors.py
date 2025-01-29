from flask import jsonify,request, Blueprint
from models import db, Editors
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 
editor_bp = Blueprint("editor_bp", __name__)

#fetch/get the editors
@editor_bp.route('/editors', methods = ['GET'])

def get_all_editors():
    # get all editors
    editors = Editors.query.all()
    #create an empty list 
    editors_list = []
    
    for edit in editors:
        editors_list.append({
            "id":edit.id,
            "blog_id":edit.blog_id,
            "user_id":edit.user_id,
            "role":edit.role
    })
    return jsonify({"Editors": editors_list})

# Get editor by id 
@editor_bp.route('/editors/<int:id>', methods = ['GET'])
# @jwt_required()
def get_editors_id(id):
    # current_user_id = get_jwt_identity()
    edit = Editors.query.get(id)
    # edit = Editor.query.filter_by(user_id = current_user_id)
    if edit:
        return jsonify({  
        "id":edit.id,
        "blog_id":edit.blog_id,
        "user_id":edit.user_id,
        "role":edit.role,
        
        # Provides the blogs title associated with the editor and user
          "blogs":
                {
                    "title":edit.blogs.title if edit.blogs else "Blog not found"                
                } 
        }), 200
    else: 
        return jsonify({"Error": "Editor does not exist"}), 404
    
#Post/create an editor 
@editor_bp.route('/editors',methods = ['POST'])
def post_editor():
    #get all the data 
    data = request.get_json()
    blog_id = data['blog_id']
    user_id = data['user_id']
    role= data['role']
    
    # check if the editor_id  exist 
    check_editor = Editors.query.filter_by(blog_id = blog_id, user_id = user_id).first()
    
    if check_editor: 
        return jsonify({"Error":"The editor already exist"}), 400
    else: 
        new_edits = Editors(blog_id = blog_id, user_id = user_id, role=role)
        db.session.add(new_edits)
        db.session.commit()
        return jsonify({"Success":"Editor added successfully"}), 201
        
        
#Update a editor based on the id
@editor_bp.route('/editors/<editor_id>', methods = ["PATCH","PUT"])
def update_editor_id(editor_id):
    # None will be the output if no editor on the database 
    # get all the Editors 
    editor= Editors.query.get(editor_id)
    
    # check if the edit exist, 
    if not editor:
        return jsonify({"Error": "Editor not found,wrong id used, Create another editor"}),404
    
    #if the data is not provided issues the data
    data = request.get_json()
    blog_id= data.get("blog_id", editor.blog_id)
    user_id = data.get("user_id",editor.user_id)
    role = data.get("role",editor.role)
    
    if blog_id==editor.blog_id and user_id==editor.user_id and role == editor.role: 
        return jsonify({"Error": "The editor with the same credential already exist"}), 406
    
# check for existing blog_id or user_id if they already exist
    check_user= Editors.query.filter(Editors.user_id==user_id and Editors.id!=editor_id).first()
    check_blog =Editors.query.filter(Editors.blog_id == blog_id and Editors.id!=editor_id).first()

#if the editor with a  user or role exist 
    if check_user or check_blog:
        return jsonify({"Error": "The editor with the blog_id, and user_id already exist. Try a different role, or user"}),406
    else: 
    #if no conflict update 
        editor.blog_id = blog_id 
        editor.user_id = user_id
        editor.role = role

    # and commit the function 
        db.session.commit()
        return jsonify({"Success": f"Editor with {user_id} is updated successfully"}),200
    
    # Password Hash
    
#Delete Editor   
@editor_bp.route('/editors/<int:user_id>' ,methods=['DELETE'])      
def delete_editors(user_id):
    #get the all the users
    editor= Editors.query.get(user_id)
    if editor:
        db.session.delete(editor)
        db.session.commit()
        return jsonify({"Success":"Editor deleted successfully"})
    else:
         return jsonify({"Error": "Editor does not exist"}), 406

# # Delete All editors
# @editor_bp.route('/editors', methods=['DELETE'])      
# def delete_all_editor():
#     #get the all the users
#     user = Editors.query.delete()
#     db.session.commit()
#     return jsonify({"Success":"Editors deleted successfully"})
        
