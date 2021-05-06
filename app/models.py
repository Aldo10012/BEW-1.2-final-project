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

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer,     primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)    # MUST be entered. MUST be unique
    password = db.Column(db.String(200), nullable=False)                 # MUST be entered
    age      = db.Column(db.Integer,     nullable=False)

    # add relationship with Pokemon
    # pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
    pokemons = db.relationship('Pokemon',  back_populates='user')     # a User can have many Pokemon


class Pokemon(UserMixin, db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    nick_name    = db.Column(db.String(100))
    weight       = db.Column(db.Float(precision=2), nullable=False)
    pokemon_type = db.Column(db.Enum(Type), default=Type.NORMAL)
    photo_url    = db.Column(URLType)
    
    # add relationship with User
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    user      = db.relationship('User',  back_populates='pokemons')
    
    # add relationship with Moves
    # move_id = db.Column(db.Integer, db.ForeignKey('move.id'))
    moves = db.relationship('Move',  back_populates='pokemon')             # a Pokemon can have many Moves


class Move(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    move_type = db.Column(db.Enum(Type), default=Type.NORMAL)
    power = db.Column(db.Integer)

    # add relationship with Pokemon
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
    pokemon    = db.relationship('Pokemon',  back_populates='moves')



# move_list_table = db.Table('move_list',
#     db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
#     db.Column('move_id', db.Integer, db.ForeignKey('move.id'))
# )

# pokemon_list_table = db.Table('pokemon_list',
#     db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )