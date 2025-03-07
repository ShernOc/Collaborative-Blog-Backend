from flask_migrate import Migrate
from flask import Flask, jsonify
from models import db
from flask_jwt_extended import JWTManager
from flask_mail import Mail,Message
from datetime import timedelta
from flask_cors import CORS
import os

#create a flask class 
app = Flask(__name__)

CORS(app)


# CORS(app, origins=["http://127.0.0.1:5000","https://collaborative-blog-backend.onrender.com","http://127.0.0.1:5173"])
CORS(app, origins=["http://localhost:5173"]) 

# #create a migration. config parameters
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# #initialize the router 
migrate = Migrate(app,db)
db.init_app(app)

#import all the functions in views 
# folder for views 
from views import * 

#register all the  blueprints 
app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(editor_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(auth_bp)



@app.route('/api/data')
def data():
    return jsonify({'message': 'Hello from JSON'})

@app.route('/')
def index(): 
    return jsonify ({"Success" :"Collaborative Blogging Platform"})

#Authentication / jw_t 
app.config["JWT_SECRET_KEY"]= os.getenv("JWT_SECRET_KEY","Sherlyne-23456")
#Toke Expire in 2 hours 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

jwt=JWTManager(app)
jwt.init_app(app)


# # Mail Credentials 
# # SMTP credentials
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'sherlynea8622@gmail.com'
# app.config['MAIL_DEFAULT_SENDER'] = 'sherlynea8622@gmail.com'
# app.config['MAIL_PASSWORD'] = 'slim hbpc dwit bsli'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

# #initialize 
# mail = Mail(app)

# #create an instance of Message 
# @app.route('/send_email')
# def email():
#     try: 
#         msg = Message(
#         subject = "First Email!",
#         sender = ['MAIL_DEFAULT_SENDER'],
#         recipients= ["sherlyne.ochieng@student.moringaschool.com","david.kakhayanga@student.moringaschool.com" ],
#         #What the message body will send
#         body = "Hello: You are welcomed to join collaborative Blogging platform")
        
#         mail.send(msg)
#         return jsonify({"Success": "Message sent Successfully"
#             })

#     except Exception as e: 
#         return jsonify({"Error" :"Message not sent"})

#run the app.py 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
