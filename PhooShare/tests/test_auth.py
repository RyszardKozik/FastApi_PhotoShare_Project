import os
import sys
import unittest
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.auth_utils import authenticate_user
from main import app

class TestAuth(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client before each test.
        """
        self.client = TestClient(app)

    def test_login(self):
        """
        Test the login endpoint.
        """
        response = self.client.post('/auth/token', data={'username': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
