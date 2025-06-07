"""Test cases for the Flask application."""
import unittest
import json
from app import app, db, Record


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up test client and database."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.client.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_route(self):
        """Test the index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, World!!!!!!")

    def test_add_record_success(self):
        """Test adding a record successfully."""
        test_record = {
            'title': 'Test Title',
            'content': 'Test Content'
        }
        response = self.client.post(
            '/api/records',
            data=json.dumps(test_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], test_record['title'])
        self.assertEqual(data['content'], test_record['content'])
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_add_record_missing_fields(self):
        """Test adding a record with missing fields."""
        test_record = {'title': 'Test Title'}  # Missing content
        response = self.client.post(
            '/api/records',
            data=json.dumps(test_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()