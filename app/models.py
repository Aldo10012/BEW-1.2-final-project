from app import db
from sqlalchemy_utils import URLType
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)


class Type(FormEnum):
    NORMAL = 'Normal'
    FIRE = 'Fire'
    WATER = 'Water'
    GRASS = 'Grass'
    ELECTRIC = 'Electric'
    ICE = 'Ice'
    FIGHTING = 'Fighting'
    POISION = 'Poison'
    GROUND = 'Ground'
    FLYING = 'Flying'
    PSYCHIC = 'Psychic'
    BUG = 'Bug'
    ROCK = 'Rock'
    GHOST = 'Ghost'
    DARK = 'Dark'
    DRAGON = 'Dragon'
    STEEL = 'Steel'
    FAIRY = 'Fairy'

# User model
class User(UserMixin, db.Model):
    id       = db.Column(db.Integer,     primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)    # MUST be entered. MUST be unique
    password = db.Column(db.String(200), nullable=False)                 # MUST be entered
    age      = db.Column(db.Integer,     nullable=False)

    pokemons = db.relationship('Pokemon', back_populates='id')         # a User can have many Pokemon

# pokemon model
class Pokemon(UserMixin, db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    nick_name    = db.Column(db.String(100))
    weight       = db.Column(db.Float(precision=2), nullable=False)
    pokemon_type = db.Column(db.Enum(Type), default=Type.NORMAL)
    photo_url    = db.Column(URLType)

    moves = db.relationship('Move', back_populates='id')              # a Pokemon can have many Moves

# move model
class Move(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    move_type = db.Column(db.Enum(Type), default=Type.NORMAL)
    power = db.Column(db.Integer)

