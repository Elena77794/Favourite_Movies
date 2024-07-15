from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, validators


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating out of 10 e.g. 7.5")
    review = StringField("Your Review")
    done = SubmitField("Done")


class AddMovie(FlaskForm):
    movie_title = StringField("Movie Title")
    add = SubmitField("Add Movie")



