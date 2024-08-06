import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.models import Rating, User, Image
from src.repository.ratings import (
    create_rate,
    delete_rate,
    calculate_rating,
    show_images_by_rating
)

class TestRatings(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Set up a MagicMock for the SQLAlchemy session and a test user
        self.session = MagicMock(spec=Session)
        self.test_user = User(
            id=1,
            login='SuperUser',
            email='user@super.com',
            password_checksum='superpwd',
            is_active=True,
        )

    def tearDown(self):
        # Clean up the session and user after each test
        self.session = None
        self.test_user = None

    async def test_create_rate_own_image(self):
        # Test: Users cannot rate their own images
        self.session.query().filter().order_by().first.return_value = Image(
            id=1,
            image_url='test_image',
            description='test_path',
            user_id=1,  # Same as test_user.id
        )
        with self.assertRaises(HTTPException) as exc_info:
            await create_rate(image_id=1, rate=5, db=self.session, user=self.test_user)
        self.assertEqual(exc_info.exception.status_code, 403)
        self.assertEqual(str(exc_info.exception.detail), "Users cannot rate their own images.")

    async def test_create_rate_twice(self):
        # Test: Users cannot rate an image twice
        self.session.query().filter().order_by().first.return_value = Rating(
            id=1,
            image_id=2,
            rate=5,
            user_id=1,  # Same as test_user.id
        )
        with self.assertRaises(HTTPException) as exc_info:
            await create_rate(image_id=2, rate=5, db=self.session, user=self.test_user)
        self.assertEqual(exc_info.exception.status_code, 423)
        self.assertEqual(str(exc_info.exception.detail), "It`s not possible to rate twice.")

    async def test_create_rate_image_not_exists(self):
        # Test: Error if the image does not exist
        self.session.query().filter().order_by().first.return_value = None
        with self.assertRaises(HTTPException) as exc_info:
            await create_rate(image_id=999, rate=5, db=self.session, user=self.test_user)
        self.assertEqual(exc_info.exception.status_code, 404)
        self.assertEqual(str(exc_info.exception.detail), "Image not found.")

    async def test_create_rate(self):
        # Test: Successfully rate an image
        self.session.query().filter().order_by().first.side_effect = [
            None,  # No existing rating
            Image(
                id=2,
                image_url='test_image',
                description='test_path',
                user_id=2,  # Different user ID
            )
        ]
        result = await create_rate(image_id=2, rate=5, db=self.session, user=self.test_user)
        self.assertIsInstance(result, Rating)

    async def test_delete_rate(self):
        # Test: Successfully delete a rate
        self.session.query().filter().order_by().first.return_value = Rating(
            id=1,
            image_id=1,
            rate=5,
            user_id=1,  # Same as test_user.id
        )
        result = await delete_rate(rate_id=1, db=self.session, user=self.test_user)
        self.assertIsNone(result)

    async def test_calculate_rating(self):
        # Test: Calculate average rating of an image
        mock_query = self.session.query.return_value
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.scalar.return_value = 4.5  # Mocked average rating

        result = await calculate_rating(image_id=1, db=self.session)
        self.assertEqual(result, 4.5)

    async def test_show_images_by_rating(self):
        # Test: Retrieve images sorted by rating
        self.session.query().filter().order_by().all.return_value = [
            Image(id=1, image_url='test_image_1', description='test_path_1', user_id=1),
            Image(id=2, image_url='test_image_2', description='test_path_2', user_id=2)
        ]
        result = await show_images_by_rating(True, db=self.session, user=self.test_user)
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
