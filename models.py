from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    movie_links = db.relationship('UserMovie', back_populates='user')


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.Text)

    # Link Movie to User  in this case it is the creator of the database entry
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user_links = db.relationship('UserMovie', back_populates='movie')

# the join table for user and movie
class UserMovie(db.Model):
    __tablename__ = 'user_movies'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)

    # this movie name could be the original or a user defined one
    custom_movie_name = db.Column(db.String(100))

    user = db.relationship('User', back_populates='movie_links')
    movie = db.relationship('Movie', back_populates='user_links')
