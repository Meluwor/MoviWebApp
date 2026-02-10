from models import db, User, Movie



class DataManager():
    # Define Crud operations as methods
    pass

def create_user(self, name):
  new_user = User(name=name)
  db.session.add(new_user)
  db.session.commit()