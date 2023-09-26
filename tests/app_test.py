import unittest
from app import app, db
from models import User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_blogly_test'
app.config['TESTING'] = True

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
    def tearDown(self):
        with app.app_context():
            db.drop_all()
    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    def test_add_user_page(self):
        response = self.client.get("/users/new")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
