from models import db, User, Movie, UserMovie


class DataManager:

    def create_user(self, name):
        """
        This function will create a user
        """
        new_user = User(name=name)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def get_user(self, user_id):
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
            return user.movie_links
        return []

    def add_movie(self, user, movie):
        """
        This function will add a movie to favorites.
        """
        try:
            db.session.add(movie)
            db.session.flush() #this generates the movie_id
    
            # link movie to user
            new_link = UserMovie(user=user, movie=movie, custom_movie_name=movie.name)
            db.session.add(new_link)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def update_movie(self,user, movie_id, new_title):
        """
        This function will update the name of a movie.
        """
        movie = Movie.query.get(movie_id)
        link = UserMovie.query.filter_by(user_id=user.id, movie_id=movie_id).first()
        if link:
            if link.custom_movie_name == new_title:
                # no changes so just return
                return
            try:
                link.custom_movie_name = new_title
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error while updating movie name. {e}")


    def delete_movie(self, user_id, movie_id):
        """
        This function will delete a movie.
        """
        link = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if link:
            try:
                movie = link.movie
                db.session.delete(link)

                db.session.flush()# is needed to be able to do propper check
                if not movie.user_links:
                    #no user uses this movie anymore
                    db.session.delete(movie)
                    print(f"Movie '{movie.name}' has been deleted from database.")
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error while deleting movie:{e}")

    def convert_movie_data(self, user_id, movie_data):
        """
        This function shall ensure to collect all the data which are needed for database.
        """
        movie_name = movie_data.get("Title")
        movie_year = movie_data.get("Year")
        movie_director = movie_data.get("Director")
        movie_poster = movie_data.get("Poster")

        new_movie = Movie()
        new_movie.name = movie_name
        new_movie.year = movie_year
        new_movie.poster_url = movie_poster
        new_movie.director = movie_director
        new_movie.user_id = user_id
        return new_movie

    def create_fake_movie(self, user_id, movie_name, movie_year):
        """
        This function will add a "fake" movie based on no data from API.
        """
        new_movie = Movie()
        new_movie.name = movie_name
        new_movie.year = movie_year
        new_movie.poster_url = ""
        new_movie.director = "N/A"
        new_movie.user_id = user_id
        return new_movie

    def does_this_movie_exist(self, movie_name):
        """
        This function will check if a movie name exists in database.
        """
        return Movie.query.filter_by(name=movie_name).first()

    def link_movie_to_user(self,user,movie):
        """
        This function shall ensure to add an existing movie to favourites
        """
        new_link = UserMovie(user=user, movie=movie, custom_movie_name=movie.name)
        try:
            db.session.add(new_link)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
