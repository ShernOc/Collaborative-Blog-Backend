from flask import jsonify,request, Blueprint
from models import db, Blog
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

#Blue print 

blog_bp = Blueprint("blog_bp", __name__)

#Get all blogs :
@blog_bp.route('/blogs', methods = ['GET'])
@jwt_required()
def get_blogs():
    # get all the blogs
    current_user_id = get_jwt_identity()
    blogs = Blog.query.all()
    
    #create an empty list to store the blogs
    blog_list= []
    # if logged in show case the blogs 
    if current_user_id: 
        for blog in blogs:
            blog_list.append({ 
            "id": blog.id,
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
            }) 
        return jsonify({"All blogs":blog_list}), 200
    else: 
         return jsonify({"Error": "Login to view the blogs"}),400 

# Get blogs by current_user_id :This is private requires an id. 
@blog_bp.route('/blogs/all', methods=['GET'])
@jwt_required()
def get_blog_id():
    current_user_id = get_jwt_identity()
    
    # get a single blog post that belongs to the currently logged-in user.
    blogs = Blog.query.filter_by(user_id=current_user_id).all()
    if not blogs: 
        return jsonify({"Error": "You have no Blogs. Create a blog"}), 404
   
    blog_list = [{  
        "id":blog.id,
        "title":blog.title,
        "content":blog.content,
        "user_id": blog.user_id,
        "is_published":blog.is_published,
        }
    for blog in blogs
    ]
    
    return jsonify({"You blogs": blog_list})
       
#Create a blog
# still need to be authenticated and need to be logged in. 
@blog_bp.route('/blogs', methods = ["POST"])
@jwt_required()
def post_blog_id():
    current_user_id = get_jwt_identity()
    
    if not blog.edit
    # get the data
    data = request.get_json()
    title = data["title"]
    content = data["content"]
    is_published= data["is_published"]
    
    #Check title or user_id of the blog exist and if error message. 
    # check_title =Blog.query.filter_by(Blog.title==title and Blog.user_id !=current_user_id)
    check_title = Blog.query.filter(Blog.title==title).first()
    check_content = Blog.query.filter(Blog.content==content).first()

    if check_title and check_content:
        return jsonify({"Error":"The blog already exist or posted"}), 406
    else: 
        #create a new blog
        new_blog = Blog(title=title,user_id=current_user_id,content=content, is_published=is_published)
        
        #call the function 
        db.session.add(new_blog)
        db.session.commit()
        return jsonify({"Success":"Blog added successfully"}), 201
      
#Update a Blog 
# Update a blog only if you are logged in.  
@blog_bp.route('/blogs/update', methods = ["PATCH","PUT"])
@jwt_required()
def update_blog_id():
    current_user_id = get_jwt_identity()
    # None if no blogs in the system. 
    # get all the Users 
    blog= Blog.query.get(current_user_id)
    
    # check if the user exist, 
    if not blog:
        return jsonify({"Error": "Blog not found. Please check the ID."}), 404
    
    #if the data is not provided issues the data
    data = request.get_json()
    title = data.get("title", blog.title)
    content = data.get("content", blog.content)
    is_published= data.get("is_published", blog.is_published)      
             
    # check for existing title or blog_id if they already exist
    check_title = Blog.query.filter(Blog.title==title).first()
    check_content= Blog.query.filter(Blog.content==content).first()
        
    #if the blog with title or user-id exist 
    if check_title and check_content:
        return jsonify({"Error":"A blog with this title and already exist. Update the blog"}),409
    else: 
        #if no conflict update 
        blog.title = title
        blog.content = content
        blog.user_id = current_user_id  
        blog.is_published = is_published 
            
        #commit the function 
        db.session.commit()
    return jsonify({"Success":f"Blog with id of {blog} was updated successfully"}),200

# Delete blog only by the user 
@blog_bp.route('/blogs/delete/<int:blog_id>',methods=['DELETE']) 
@jwt_required()
def delete_blog(blog_id):
    current_user_id = get_jwt_identity()
    #check blog
    
    blog =Blog.query.filter_by(id = blog_id, user_id=current_user_id).first()
    
    if not blog:
        return jsonify({"Error": "Blog not found, authorized"}), 406 
    
    db.session.delete(blog)
    db.session.commit()
    
    return jsonify({"Success": f"A Blog with has been deleted Successfully"})

# Done by the Admin
# #Delete all blogs
# @blog_bp.route('/blogs/delete' ,methods=['DELETE'])  
#@jwt_required()
# def delete_all_blog():
    #current_user_id = get
#     #get the all the blogs
#     blog = Blog.query.delete()
#     db.session.commit()
#     return jsonify({"Success":"Blogs have been deleted successfully"})


      