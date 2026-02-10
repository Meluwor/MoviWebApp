from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DATE
from sqlalchemy.dialects.mysql import VARCHAR

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Movie(db.Model):
    # Define all the Movie properties
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    director = db.Column(db.String(100))
    year = db.Column(db.Date)
    poster_url = db.Column(db.Text)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def main():
    """
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL);
    :return:
    """
    pass

if __name__=="__main__":
    main()