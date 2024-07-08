from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import mysql.connector
import os

connection = mysql.connector.connect(user='root',
                                     host='localhost',
                                     port="3306")

my_cursor = connection.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

# CREATE DB
# my_cursor.execute("CREATE DATABASE IF NOT EXISTS Top_Movie_Web")

# Select the Database
my_cursor.execute("USE Top_Movie_Web")

# CREATE TABLE
# my_cursor.execute("CREATE Table IF NOT EXISTS Movie(id INT NOT NULL AUTO_INCREMENT, "
#                   "title VARCHAR(100) NOT NULL UNIQUE,"
#                   " year YEAR NOT NULL,"
#                   " description VARCHAR(1000) NOT NULL, "
#                   "rating DOUBLE NOT NULL, "
#                   "ranking INT NOT NULL, "
#                   "review VARCHAR(500) NOT NULL, "
#                   "img_url VARCHAR(1000) NOT NULL,"
#                   "PRIMARY KEY (id))")


# Insert New Movie
def insert_new_movie(connection, movie):
    my_cursor = connection.cursor()
    query = ("INSERT INTO Movie (title, year, description, rating, ranking, review, img_url)"
             "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    data = (
    movie["movie_name"], movie["year"], movie["description"], movie["rating"], movie["ranking"], movie["review"],
    movie["img_url"])
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


# Retrieve all movies from database
def get_all_movies():
    my_cursor = connection.cursor()
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

data_movie = get_all_movies()


@app.route("/")
def home():
    return render_template("index.html", data_movie=data_movie)


# Close the connection
my_cursor.close()
connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=4005)


