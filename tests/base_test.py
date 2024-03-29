"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # runs once for each test case
        #
        # sqlite doesn't enforce foreign key constraints, so tests would pass without store table created etc
        # so better to use postgresq / final database to get a failure
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'

        # Setting debug false, otherwise, flask will think there's an error, initializing the
        # db after app has already been initialized
        # Then, also need to set propagate exceptions - to make it so when an exception happens in code, it
        # bubbles up in flask hierarchy and is caught up by the error handlers (normally set automatically if debug = T)
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True

        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Runs once for every test method
        #
        # Make sure database exists

        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
