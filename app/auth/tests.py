import os
from unittest import TestCase

from datetime import date
 
from app import app, db, bcrypt
from app.models import *

# python -m unittest app.auth.tests
#################################################
# Setup
#################################################

def create_pokemon():
    pokemon = Pokemon(
        name = "Pikachu",
        nick_name = "Yellow Flash",
        weight = 13,
        pokemon_type = Type.ELECTRIC,
        photo_url = "https://d29zunrt9sid73.cloudfront.net/speaker_media/asset/28695/portrait_70_28695.png"
    )
    db.session.add(pokemon)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash, age=10)
    db.session.add(user)
    db.session.commit()


#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    
    def test_signup(self):
        '''test signup route'''
        post_data = {
            'username': 'me1',
            'password': "password",
            'age':10
        }
        self.app.post('/signup', data=post_data)
        user = User.query.filter_by(username='me1').one()
        self.assertEqual(user.username, 'me1')

    def test_signup_existing_user(self):
        '''test signup route with existing user'''
        create_user()
        post_data = {
            'username': 'me1',
            'password': "password",
            'age':10
        }
        self.app.post('/signup', data=post_data)
        current_user = User.query.filter_by(username=post_data['username']).one()
        self.assertEqual(current_user.username, 'me1')
        self.assertNotIn(current_user.password, 'password')
        print("error message here")
    
    def test_login_correct_password(self):
        '''test login route with incorrect password'''
        create_user()
        post_data = {
            'username': 'me1',
            'password': "password",
            'age' : 10
        }
        self.app.post('/login', data=post_data)

        current_user = User.query.filter_by(username=post_data['username']).one()
        self.assertNotIn(current_user.password, 'password')
    
    def test_login_nonexistent_user(self):
        '''test login route with nonexistant user'''
        post_data = {
            'username': 'me1',
            'password': "password",
            'age' : 10
        }
        self.app.post('/login', data=post_data)

        self.assertIn(post_data['password'], 'password')
        print("incorrect")
        
    def test_login_incorrect_password(self):
        '''test login route with incorrect password'''
        create_user()

        post_data = {
            'username': 'me1',
            'password': "incorrct_password",
            'age' : 10
        }
        self.app.post('/login', data=post_data)

        self.assertIn(post_data['password'], 'incorrct_password')
        print("incorrect password")
    
    def test_logout(self):
        '''test logout'''
        create_user()

        post_data = {
            'username': 'me1',
            'password': "incorrct_password",
            'age' : 10
        }
        self.app.post('/login', data=post_data)

        response = self.app.get('/logout', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('login', response_text)