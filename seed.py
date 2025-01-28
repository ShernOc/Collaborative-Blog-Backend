from faker import Faker
from faker import Faker
from models import db, User, Blog,Editors,Comment, db

#Next is to add the dates
# Commented out the Dates will be updated in the next work. 

#initialize
fake = Faker()
#Default numbers of fake data = 15 
roles = ["editor", "viewer"]
users = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
blogs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

# creating random fake date for users
def user_data():
    num_records = 15
    with app.app_context():  
        try:
            for _ in range(num_records):
                user = User(
                # Replace with your model's fields,
                name=fake.name(),
                email=fake.email(),
                password = fake.password(),
                is_admin=fake.boolean())
                db.session.add(user)

                # Commit to the database
                db.session.commit()
                print(f"{num_records} Users added to the database!")
        except Exception as e:
                print("An error occurred:", e)
                db.session.rollback() 
        
# Create random data for blog
def blog_data():
    num_records = 15
    with app.app_context():
          
        try:
            #fetching existing users and comments 
            
                for _ in range(num_records):
                    blog=Blog(
                    title=fake.sentence(nb_words=5),       
                    content=fake.text(max_nb_chars=50),
                    user_id=fake.random_element(users),
                    # date=fake.date_time_this_year().strftime("%d/%m/%Y"),
                    is_published=fake.boolean()
                )
                    db.session.add(blog)
                    db.session.commit()
                    print(f"{num_records} Blogs added to the database!")
        except Exception as e:
                print("An error occurred:", e)
                db.session.rollback() 
    
def editor_data():
    # Number of records to generate
    num_records = 5
    with app.app_context(): 
        try: 
           
        # Create random data for editors
            for _ in range(num_records):
                edit = Editors(
                    blog_id = fake.random_element(blogs),
                    user_id = fake.random_element(users),
                    role=fake.random_element(roles))
                   
                db.session.add(edit)

                # Commit to the database
                db.session.commit()
                print(f"{num_records} Success, editors updated safely")
        
        except Exception as e:
            print("An error occurred:", e)
            db.session.rollback() 

def comment_data():
    # Number of records to generate
    num_records = 7
    
    with app.app_context(): 
        try:  
        # Create random data for editors
        
            for _ in range(num_records):
                comment = Comment(
                    # date = fake.date_time_this_year().strftime("%d/%m/%Y"),
                    content = fake.text(),
                    user_id = fake.random_element(users),
                    blog_id = fake.random_element(blogs)
            )
                db.session.add(comment)

                # Commit to the database
                db.session.commit()
                print(f"{num_records} Success, comment updated safely" )
        
        except Exception as e:
            print("An error occurred:", e)
            db.session.rollback()

# if __name__ == "__main__":
#     # # user_data()
#     # blog_data()
#     # # editor_data()
#     # # comment_data()
    