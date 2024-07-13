from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import requests
from sql_connection import get_sql_connection
import os
from forms import RateMovieForm, AddMovie



# Connect to database
connection = get_sql_connection()
my_cursor = connection.cursor()

KEY_DATABASE_MOVIE = os.getenv(KEY_DATABASE_MOVIE)


app = Flask(__name__)
app.config['SECRET_KEY'] = "any-string-you-want-just-keep-it-secret"
Bootstrap5(app)


# Create database
# my_cursor.execute("CREATE DATABASE IF NOT EXISTS Top_Movie_Web")

# Select the database
my_cursor.execute("USE Top_Movie_Web")

# Create table in Database
# my_cursor.execute("CREATE Table IF NOT EXISTS Movie(id INT NOT NULL AUTO_INCREMENT, "
#                   "title VARCHAR(100) NOT NULL UNIQUE,"
#                   "year YEAR NOT NULL,"
#                   " description VARCHAR(1000) NOT NULL, "
#                   "rating DOUBLE,"
#                   "ranking INT,"
#                   "review VARCHAR(500) NOT NULL, "
#                   "img_url VARCHAR(1000) NOT NULL,"
#                   "PRIMARY KEY (id))")


# Insert new movie in your database
def insert_new_movie(connection, movie):
    my_cursor = connection.cursor()
    query = ("INSERT INTO Movie (title, year, description, img_url)"
             "VALUES (%s, %s, %s, %s)")

    data = (
    movie["movie_name"], movie["year"], movie["description"], movie["img_url"])
    my_cursor.execute(query, data)
    connection.commit()
    return my_cursor.lastrowid



# insert_new_movie(connection, {"movie_name": "Phone Booth",
#                               'year': 2002,
#                               "description": "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#                               "rating": 7.3,
#                               "ranking": 10,
#                               "review": "My favourite character was the caller.",
#                               "img_url": "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg" })
#

# Retrieve all movies from database
def get_all_movies(connection):
    query = ("SELECT id, title, year, description, rating, ranking, review, img_url FROM Movie")
    my_cursor.execute(query)
    response = []
    for id, title, year, description, rating, ranking, review, img_url in my_cursor:
        if isinstance(img_url, bytes):
            img_url = img_url.decode('utf-8')
        response.append({"id": id,
                         "title": title,
                         "year": year,
                         "description": description,
                         "rating": rating,
                         "ranking": ranking,
                         "review": review,
                         "img_url": img_url})
    return response




# Update rating and review movie in database
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_button(id):
    form = RateMovieForm()
    # Display the title Movie
    query = "SELECT title FROM Movie WHERE id = %s"
    my_cursor.execute(query, (id,))
    title = my_cursor.fetchone()[0]
    if form.validate_on_submit():
        rating = form.rating.data
        review = form.review.data
        update_query = "UPDATE Movie SET rating=%s, review=%s WHERE id=%s"
        my_cursor.execute(update_query, (rating, review, id))
        connection.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, title=title)


# Delete unwanted movie from your database
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_movie(id):
    query = "DELETE FROM Movie WHERE id = %s"
    my_cursor.execute(query, (id,))
    connection.commit()
    return redirect((url_for("home")))



# Display all movies from database on index.html
@app.route("/")
def home():
    data_movie = get_all_movies(connection)
    return render_template("index.html", data_movie=data_movie)


# Fetch movie data from the API by title and display all results on select.html
@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovie()
    if form.validate_on_submit():
        movie_title = form.movie_title.data
        url = "https://api.themoviedb.org/3/search/movie?include language=en-US&"
        headers ={
            "accept": "application/json",
            "Authorization": f"Bearer {KEY_DATABASE_MOVIE}"
            }
        # Make request
        response = requests.get(url, params={"query": movie_title}, headers=headers)
        data = response.json()
        movies = data["results"]
        # Render the results on select.html
        return render_template("select.html", movies=movies)
    return render_template("add.html", form=form)



# Select movie by id on select.html and insert in database
@app.route("/select/<int:movie_id>", methods=["GET", "POST"])

def select_movie(movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {KEY_DATABASE_MOVIE}"
        }

        # Make request and receive the data of img_url, title, description and release date
        response = requests.get(url, params={"movie_id": movie_id, "language": "en-US"}, headers=headers)
        data = response.json()
        title = data['title']
        data_img_url = data['poster_path']
        MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
        img_url = f"{MOVIE_DB_IMAGE_URL}{data_img_url}"
        description = data['overview']
        date_string = data['release_date']
        year = date_string.split('-')[0]

        # Insert the data in database
        insert_movie = insert_new_movie(connection, {"movie_name": title,
                                      'year': year,
                                      "description": description,
                                      "img_url": img_url})
        if insert_movie:
            query = f"SELECT id FROM Movie WHERE title = %s"
            my_cursor.execute(query, (title,))
            movie_id = my_cursor.fetchone()[0]

        return redirect(url_for('edit_button', id=movie_id))


# # Close the connection
my_cursor.close()
connection.close()


if __name__ == '__main__':
    app.run(debug=True, port=4005)


