from models import db, User, Movie


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
            return user.movies
        return []

    def add_movie(self, user, movie):
        """
        This function will add a movie to favorites.
        """
        try:
            user.movies.append(movie)
            db.session.add(movie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

    def update_movie(self, movie_id, new_title):
        """
        This function will update the name of a movie.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            if movie.name == new_title:
                # no changes so just return
                return
            try:
                movie.name = new_title
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")

    def delete_movie(self, user_id, movie_id):
        """
        This function will delete a movie.
        """
        movie = Movie.query.get(movie_id)
        user = self.get_user(user_id)
        if movie and user:
            if movie in user.movies:
                try:
                    user.movies.remove(movie)
                    if not movie.users:
                        db.session.delete(movie)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error: {e}")

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

    def link_movie_to_user(self):
        """
        This function shall ensure to add an existing movie to favourites
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
