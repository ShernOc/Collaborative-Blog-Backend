from flask import jsonify,request, Blueprint
from models import db, Comment
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 

comment_bp = Blueprint("comment_bp", __name__)

#fetch/get the comments if logged in 
@comment_bp.route('/comments', methods =['GET'])
@jwt_required()
def get_all_comments():
    current_user_id = get_jwt_identity()
    # get all comments 
    comments = Comment.query.filter_by(user_id=current_user_id)
    #create an empty list 
    comments_list = []
    if current_user_id:
        for comment in comments :
            comments_list.append({
                "id":comment.id,
                "content":comment.content,
                "user_id":comment.user_id,
                "blog_id":comment.blog_id
        })
        return jsonify({"All Comments":comments_list})

# Get comments by id 
@comment_bp.route('/comments/<int:comment_id>', methods = ['GET'])
@jwt_required()
def get_comments_id(comment_id):
    current_user_id = get_jwt_identity()
    comment = Comment.query.filter_by(id=comment_id, user_id = current_user_id).first()
    # comment = Editor.query.filter_by(user_id = current_user_id)
    if comment:
        return jsonify({  
        "id":comment.id,
        "blog_id":comment.blog_id,
        "user_id":comment.user_id,
        "content":comment.content,
        
        # Provides the blog associated with the comment and user
          "blogs":
                {
                    "title":comment.blogs.title if comment.blogs else "Blog not found"                
                } 
        }), 200
    else: 
        return jsonify({"Error": "Comment does not exist"}), 404
    
#Post/create an comment
@comment_bp.route('/comments', methods = ['POST'])
@jwt_required()
def post_comments():
    current_user_id = get_jwt_identity()
    #get all the data 
    data = request.get_json()
    blog_id = data['blog_id']
    content=data['content']
    
    # check if the editor_id  exist 
    check_content = Comment.query.filter_by(content = content, user_id = current_user_id).first()
    
    if check_content: 
        return jsonify({"Error":"The comments already exist"}), 400
    else: 
        new_comment = Comment(blog_id = blog_id, user_id = current_user_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"Success":"Comment added successfully"}), 201
        
        
#Update a comment based on the id
@comment_bp.route('/comments/<comment_id>', methods = ["PATCH","PUT"])
@jwt_required()
def update_comments_id(comment_id):
    current_user_id = get_jwt_identity()
    # None will be the output if no comment on the database 
    # get all the Comments
    comment= Comment.query.get(comment_id)
    
    # check if the comment exist, 
    if not comment or comment.user_id !=current_user_id:
        return jsonify({"Error": "Comment not found,wrong id used, Create another editor"}),404
    
    #if the data is not provided issues the data
    data = request.get_json()
    blog_id= data.get("blog_id", comment.blog_id)
    user_id = data.get("user_id",comment.user_id)
    content = data.get("content",comment.content)
    
    if blog_id==comment.blog_id and user_id==comment.user_id and content == comment.content: 
        return jsonify({"Error": "The comment with the same credential already exist"}), 406
    
# check for existing blog_id or user_id if they already exist
    check_content= Comment.query.filter(Comment.content==content and Comment.id!=comment_id).first()

#if the comment with a  user or role exist 
    if check_content:
        return jsonify({"Error": "The comment with the same content, already exist. Write a different content"}),406
    else: 
    #if no conflict update 
        comment.blog_id = blog_id 
        comment.user_id = current_user_id
        comment.content= content

    # and commit the function 
        db.session.commit()
        return jsonify({"Success": f"Comment with {comment_id} is updated successfully"}),200
    
#Delete a Comment  
@comment_bp.route('/comments/<int:comment_id>' ,methods=['DELETE'])   
@jwt_required()
def delete_Comment(comment_id):
    #get the all the users
    current_user_id=get_jwt_identity()
    comment= Comment.query.filter_by(id = comment_id,user_id=current_user_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"Success":"Comment deleted successfully"})
    else:
         return jsonify({"Error": "comment with that id does not exist"}), 406

# # # Delete All comments 
# # @comment_bp.route('/comments ', methods=['DELETE'])      
# # def delete_all_comments():
# #     #get the all the comments
# #     comments = Comment.query.delete()
# #     db.session.commit()
# #     return jsonify({"Success":"Comments deleted successfully})

