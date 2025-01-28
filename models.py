from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Enum
from sqlalchemy.orm import validates 
from datetime import datetime



metadata = MetaData()

db = SQLAlchemy(metadata=metadata)
ROLE_ENUM = ('editor', 'reviewer')

#Concept: 
# A user can write many blogs
#A user can also comment on the blog

#Next installation be able to add the Dates. 

#User  Table 
class User(db.Model):
    __tablename__ = "users"
    #User table 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    
    #A user write many blogs
    #relationships
    blogs = db.relationship("Blog", back_populates = "users", lazy =True)
    editors = db.relationship("Editors", back_populates="users", lazy=True)
    comments =db.relationship("Comment", back_populates = "users", lazy = True)
    
# email validation 
@validates("email")
def validate_email(self,key,email):
    if "@" not in email: 
        raise ValueError("Invalid email format, include @ in your email")
    return email

#Blog table 
class Blog(db.Model):
    __tablename__= "blogs"
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False )
    content = db.Column(db.String(256), nullable = False)
    user_id= db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    # date = db.Column(db.DateTime, default = datetime.day)
    is_published = db.Column(db.Boolean, nullable = False)
    
    # relationships
    users= db.relationship("User", back_populates = "blogs", lazy = True, )
    editors = db.relationship("Editors", back_populates="blogs", lazy=True)
    comments = db.relationship("Comment", back_populates="blogs", lazy=True)


# Editors Table 
class Editors(db.Model):
    __tablename__ = "editors"
    
    id = db.Column(db.Integer, primary_key = True)
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable = False)
    role = db.Column(Enum(*ROLE_ENUM, name="role_enum"),nullable =False)
    
    # relationships 
    users= db.relationship("User", back_populates = "editors")
    blogs= db.relationship("Blog", back_populates ="editors")
    

#Comment table 
class Comment(db.Model):
    #table name 
    __tablename__ = "comments"
    #database
    id = db.Column(db.Integer, primary_key = True)
    # date = db.Column(db.DateTime, default =datetime.day)
    content = db.Column(db.String(120), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"), nullable = False)
    
    users= db.relationship("User", back_populates ="comments", lazy= True)
    blogs= db.relationship("Blog", back_populates="comments", lazy=True)
    
    
    #Logout Flask Model 
class TokenBlocklist(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        jti = db.Column(db.String(36), nullable=False, index=True)
        created_at = db.Column(db.DateTime, nullable=False)

    
    
    
# #Blog
# #Collaboration 
# #Comment 
# #hint: if not saved local storage: save the project in the local storage 
# # Collaborate on Blog: As a user, I want to invite other users to collaborate on my blog post.
# # A User can write a Comment of a Blog 
# #Being able to 
# # A User being able to publish the blog 

# print("life is good")



