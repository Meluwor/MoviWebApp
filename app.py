from flask import Flask, render_template, request, redirect, url_for, abort

from data_manager import DataManager
from models import db, Movie
import os
import OMDB_api as API
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
    user = data_manager.get_user(user_id)
    if user:
        movies = data_manager.get_movies(user_id)
        return render_template('movies.html', user_id=user_id, movies = movies)
    abort(404, description=f"There is no user by given id:{user_id}.")



@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    This route will allow a user to add a new movie to their personal favorites.
    """
    user = data_manager.get_user(user_id)
    if not user:
        abort(404, description=f"There is no user by given id:{user_id}.")

    movie_name = request.form.get('title')
    movie_year = request.form.get('year')
    if movie_name:
        movie_data = API.get_movie_by_name(movie_name, movie_year)
        if movie_data:
            new_movie = data_manager.convert_movie_data(user.id,movie_data)
            data_manager.add_movie(new_movie)
    return redirect(url_for('get_movies' , user_id=user_id))


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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    #with app.app_context():
        #db.create_all()
    API.prepare_and_check_api()
    app.run(host="0.0.0.0", port=5002, debug=True)
