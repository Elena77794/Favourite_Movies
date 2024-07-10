from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, validators


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    done = SubmitField("Done")
