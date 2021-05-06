from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import *
from app.main.forms import *
from app import bcrypt, app, db

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    if current_user.is_authenticated:
        pokemons = current_user.pokemons                            # only get the pokemon of the logged in user
        return render_template('home.html', all_pokemon=pokemons)
    return render_template('home.html', all_pokemon=[])
    
    # all_pokemon = Pokemon.query.all()
    # return render_template('home.html', all_pokemon=all_pokemon)


@main.route('/pokemon/<pokemon_id>', methods=['GET', 'POST'])
def pokemon_detail(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    form = MoveForm()

    if form.validate_on_submit():
        pokemon.moves.append(Move(
            name=form.name.data,
            move_type=form.move_type.data,
            power=form.power.data
        ))

        db.session.add(pokemon)
        db.session.commit()

        flash('New Pokemon was creates successfuly')
        return redirect(url_for('main.pokemon_detail', pokemon_id=pokemon.id), form=form)

    return render_template('pokemon_detail.html', pokemon=pokemon, form=form)


@main.route('/new_pokemon', methods=['GET', 'POST'])
@login_required
def new_pokemon():
    form = PokemonForm()
    if form.validate_on_submit():
        new_pokemon = Pokemon(
            name=form.name.data,
            nick_name=form.nick_name.data,
            weight=form.weight.data,
            pokemon_type=form.pokemon_type.data,
            photo_url=form.photo_url.data
        )
        new_pokemon.user = current_user   # adding flask_login.current_user as creator
        db.session.add(new_pokemon)
        db.session.commit()
        
        flash('success')
        return redirect(url_for('main.pokemon_detail', pokemon_id=new_pokemon.id)) 

    return render_template('new_pokemon.html', form=form)


# @main.route('/new_move', methods=['GET', 'POST'])
# @login_required
# def new_move():
#     form = MoveForm()
#     if form.validate_on_submit():
#         new_move = MoveForm(
#             name=form.name.data
#             move_type=form.move_type.data
#             power=form.power.data
#         )
#         new_move.created_by = current_user   # adding flask_login.current_user as creator
#         db.session.add(new_move)
#         db.session.commit()
        
#         flash('success')
#         return redirect(url_for('main.pokemon_detail', move_id = new_move.id)) 

#     return render_template('pokemon_detail.html', form=form)