from flask import jsonify,request, Blueprint
from models import db, Blog
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 
blog_bp = Blueprint("blog_bp", __name__)

@blog_bp.route('/blogs', methods = ['GET'])
# @jwt_required()
def get_blogs():
    # current_user_id = get_jwt_identity()
    #get all the users 
    blogs = Blog.query.all()
    
    # blogs = Blog.query.filter_by(user_id = current_user_id)
    #create an empty list to store the blogs
    blog_list= []
    
    for blog in blogs:
        blog_list.append({ 
        "id": blog.id,
        "title":blog.title,
        "content":blog.content,
        "user_id": blog.user_id,
        "is_published":blog.is_published,   
        })
    return jsonify({"All blogs":blog_list})

# Get blogs by id 
@blog_bp.route('/blogs/<int:id>', methods = ['GET'])
# @jwt_required()
def get_blog_id(id):
    # current_user_id = get_jwt_identity()
    blog = Blog.query.get(id)
    # blogs = Blog.query.filter_by(user_id = current_user_id)
    if blog:
        return jsonify({  
        "id":blog.id,
        "title":blog.title,
        "content":blog.content,
        "user_id": blog.user_id,
        "is_published":blog.is_published,
        #Provides the users associated with the blog
          "users":[
                {
                    "id":users.id,
                    "name":users.name
                    
                } for users in blog.users
            ] 
        }), 200
    else: 
        return jsonify({"Error": "Blog does not exist"}), 404


#Create a blog
@blog_bp.route('/blogs', methods = ["POST"])
def post_blog_id():
    # get the data
    data = request.get_json()
    title = data["title"]
    content = data["content"]
    user_id = data["user_id"]
    is_published= data["is_published"]
    
    #Check title or user_id of the blog exist and if error message. 
    check_title = Blog.query.filter_by(title=title).first()
    check_user = Blog.query.filter_by(user_id=user_id).first()
    
    if check_title or check_user:
        return jsonify({"Error": "The blog already posted"}), 406
    else: 
        #create a new blog
        new_blog = Blog(title=title,user_id=user_id,content=content, is_published=is_published)
        
        #call the function 
        db.session.add(new_blog)
        db.session.commit()
        return jsonify({"Success": "The blog added successfully"}), 201
      
#Update a Blog  
@blog_bp.route('/blogs/<blog_id>', methods = ["PATCH","PUT"])
def update_blog_id(blog_id):
    # blogs will be none if no blog is found
    # get all the Users 
    blog= Blog.query.get(blog_id)
    
    # check if the user exist, 
    if not blog:
        return jsonify({"Error": "Blog not found. Please check the ID."}), 404
    
    #if the data is not provided issues the data
    data = request.get_json()
    title = data.get("title", blog.title)
    content = data.get("content", blog.content)
    user_id = data.get("user_id", blog.user_id)
    is_published= data.get("is_published", blog.is_published)      
    
        
    #check if the data is the same/identical no change was made 
    if title==blog.title and content==blog.content and  is_published==blog.is_published:
        return jsonify({"Error": "Blog full data is in the database, update something else"}), 400
             
    # check for existing title or blog_id if they already exist
    check_title = Blog.query.filter_by(title=title and id!=blog_id).first()
    check_user = Blog.query.filter_by(user_id=user_id and id!=blog_id).first()
        
    #if the blog with title or user-id exist 
    if check_title or check_user:
        return jsonify({"Error": "A blog with this title or blog_id already exist. Use a different title or blog id"}),409
    
    else: 
        #if no conflict update 
        blog.title = title
        blog.content = content
        blog.user_id = user_id    
        blog.is_published = is_published 
            
        #commit the function 
        db.session.commit()
        return jsonify({"Success": f"Blog with id of {blog_id} was updated successfully"}),200
    
    # Hash the password
  
# Delete blog
@blog_bp.route('/blogs/<int:blog_id>',methods=['DELETE'])        
def delete_blog(blog_id):
    #get the all the blogs
    blog = Blog.query.get(blog_id)
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"Success":"A Blog has been deleted Successfully"})
    else:
         return jsonify({"Error": "The blog does not exist"}), 406
     
# #Delete all blogs
# @blog_bp.route('/blogs' ,methods=['DELETE'])        
# def delete_all_blog():
#     #get the all the blogs
#     blog = Blog.query.delete()
#     db.session.commit()
#     return jsonify({"Success":"Blogs have been deleted successfully"})


      