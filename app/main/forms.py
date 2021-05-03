from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from app.models import *

class PokemonForm(FlaskForm):
    '''Form to create a Pokemon'''
    name         = StringField('Type of Pokemon', validators=[DataRequired(), Length(min=3, max=80)])
    nick_name    = StringField('Give Pokemon a nick name', validators=[DataRequired(), Length(min=3, max=80)])
    weight       = FloatField('Weight', validators=[DataRequired()])
    pokemon_type = SelectField('Select a Type', choices=Type.choices(), validators=[DataRequired()])
    photo_url    = StringField('Photo_url',  validators=[URL()])
    submit       = SubmitField('Submit')

class MoveForm(FlaskForm):
    '''Form to create a Pokemon move'''
    name      = StringField('Enter name of move', validators=[DataRequired()])
    move_type = SelectField('Select a Type', choices=Type.choices(), validators=[DataRequired()])
    power     = IntegerField('How much damage', validators=[DataRequired()])
    submit    = SubmitField('Submit')