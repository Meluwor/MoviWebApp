from numpy import error_message

from models import db, User, Movie



class DataManager:

    def create_user(self, name):
        """
        This function will create a user
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_user(self,user_id):
        """
        This funktion returns a user by given id.
        """
        return User.query.get(user_id)

    def get_users(self):
        """
        This funktion returns a list of all users.
        """
        return User.query.all()

    def get_movies(self, user_id):
        """
        This function will return all movies of a specific user.
        """
        user = User.query.get(user_id)
        if user:
            return user.movies
        return []

    def add_movie(self, movie):
        """
        This function will add a movie to favorites.
        """
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """
        This function will update the name of a movie.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return True
        return False

    def delete_movie(self, movie_id):
        """
        This function will delete a movie.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False