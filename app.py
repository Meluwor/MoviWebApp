from flask import Flask, render_template
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/', methods=['GET'])
def home():
    return "Welcome to MoviWeb App!"

@app.route('/users',methods=['GET'])
def list_users():
    """
    This route will return a list of all users.
    """
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


@app.route('/users', methods=['POST'])
def add_user():
    """
    This route will allow to add a user.
    """
    return render_template("add_user.html")

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def show_favorites_of_user(user_id):
    """
    This route will show all favorites of a user.
    """
    return render_template("user_favorites.html")


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def change_movie_name(user_id,movie_id):
    """
    "This route allows users to rename any movie stored in their personal favorites."
    """
    pass

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['DELETE'])
def delete_movie(user_id,movie_id):
    """
    "This route allows users to delete any movie stored in their personal favorites."
    """
    pass


if __name__ == '__main__':
 # with app.app_context():
    #db.create_all()

  app.run()