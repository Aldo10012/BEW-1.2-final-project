import os
import unittest

from datetime import date
 
from app import app, db, bcrypt
from app.models import *

# python3 -m unittest app.main.tests
#################################################
# Setup
#################################################

def login(client, username, password, age=10):
    return client.post('/login', data=dict(
        username=username,
        password=password,
        age=age
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash, age=10)
    db.session.add(user)
    db.session.commit()

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


#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    
    def test_homepage_logged_out(self):
        """Test that the books show up on the homepage."""
        # Set up
        create_pokemon()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Pokemon', response_text)
        self.assertNotIn('Log Out', response_text)

    def test_homepage_logged_in(self):
        """Test that the books show up on the homepage."""
        # Set up
        create_pokemon()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Create Pokemon', response_text)
        self.assertIn('Log Out', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)