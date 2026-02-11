from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    This route will allow to create a user.
    """
    user_name = request.form.get('name')
    if user_name:
        data_manager.create_user(user_name)

    return redirect(url_for('index'))


@app.route('/users',methods=['GET'])
def list_users():
    """
    This route will return a list of all users.
    """
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string




@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """
    This route will show all favorites of a user.
    """
    return render_template("movies.html")


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

  app.run()
