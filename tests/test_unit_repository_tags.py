import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# Adjusting the system path to include the src directory for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
print(sys.path)  # Debugging: Print sys.path to check the paths included

from src.schemas.tags import TagModel
from src.database.models import Tag, tag_to_image, Image
from src.repository.tags import (
    parse_tags,
    create_tags,
    edit_tag,
    find_tag,
    delete_tag,
    get_images_by_tag
)

"""
Unit test repository tags.
"""

class TestTags(unittest.IsolatedAsyncioTestCase):
    """
    Unit Test Tags repository.
    """

    def setUp(self):
        """
        The setUp function is run before each test.
        It creates a mock session object, and sets up test instances for Tag and Image.
        """
        # Mocking the SQLAlchemy session
        self.session = MagicMock(spec=Session)
        # Creating a mock tag object
        self.tag = Tag(id=1, tag_name="test_tags")
        # Incoming data simulating user input
        self.incoming_data = "#test_tags"
        # Creating a mock image object
        self.image = Image(
            id=1,
            image_url="url image",
            user_id=1,
            description="test string description________________________________",
        )

    def test_parse_tags_found(self):
        """
        Test parsing tags from a string containing a hashtag.
        """
        expect_result = ["test_tags"]
        tags = parse_tags(self.incoming_data)
        self.assertEqual(tags, expect_result)
        self.assertListEqual(tags, expect_result)

    def test_parse_tags_not_found(self):
        """
        Test parsing tags when no tags are present in the string.
        """
        expect_result = list()
        incoming_data = ""
        tags = parse_tags(incoming_data)
        self.assertEqual(tags, expect_result)
        self.assertListEqual(tags, expect_result)

    async def test_create_new_tags_existing_tag(self):
        """
        Test creating tags when the tag already exists in the database.
        """
        expect_result = [self.tag]
        # Mocking the query result to return an existing tag
        self.session.query().filter().first.return_value = self.tag
        # Testing the create_tags function
        result = await create_tags(self.incoming_data, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result[0], expect_result[0])

    async def test_create_new_tags_new_tag(self):
        """
        Test creating a new tag when it doesn't exist in the database.
        """
        expect_result = [self.tag]
        # Mocking the query result to return None (no existing tag)
        self.session.query().filter().first.return_value = None
        # Mocking the add method to simulate adding the tag
        self.session.add.return_value = MagicMock(return_value=self.tag)
        with patch('src.repository.tags.Tag', return_value=self.tag):
            result = await create_tags(self.incoming_data, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result[0], expect_result[0])

    async def test_edit_tag_found(self):
        """
        Test editing an existing tag.
        """
        expect_result = self.tag
        edit_tag_name = "edit_name_tag"
        # Creating a TagModel for updating
        tag_model = TagModel(tag_name=edit_tag_name)
        # Testing the edit_tag function
        result = await edit_tag(expect_result, tag_model, db=self.session)
        self.assertEqual(result.tag_name, edit_tag_name)
        self.assertEqual(result.tag_name, expect_result.tag_name)
        self.assertEqual(result.id, expect_result.id)

    async def test_find_tag_by_id_found(self):
        """
        Test finding a tag by its ID.
        """
        expect_result = self.tag
        id_tag = self.tag.id
        # Mocking the query result to return the tag
        self.session.query().filter().first.return_value = self.tag
        # Testing the find_tag function
        result = await find_tag(id_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_find_tag_by_id_not_found(self):
        """
        Test finding a tag by its ID when it doesn't exist.
        """
        expect_result = None
        id_tag = self.tag.id
        # Mocking the query result to return None (tag not found)
        self.session.query().filter().first.return_value = None
        # Testing the find_tag function
        result = await find_tag(id_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_find_tag_found(self):
        """
        Test finding a tag by its name.
        """
        expect_result = self.tag
        tex_tag = self.tag.tag_name
        # Mocking the query result to return the tag
        self.session.query().filter().first.return_value = self.tag
        # Testing the find_tag function
        result = await find_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_find_tag_not_found(self):
        """
        Test finding a tag by its name when it doesn't exist.
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        # Mocking the query result to return None (tag not found)
        self.session.query().filter().first.return_value = None
        # Testing the find_tag function
        result = await find_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_delete_tag_found(self):
        """
        Test deleting a tag that exists.
        """
        expect_result = self.tag
        tex_tag = self.tag.tag_name
        # Mocking the query result to return the tag
        self.session.query().filter().first.return_value = self.tag
        # Testing the delete_tag function
        result = await delete_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_delete_tag_not_found(self):
        """
        Test deleting a tag that does not exist.
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        # Mocking the query result to return None (tag not found)
        self.session.query().filter().first.return_value = None
        # Testing the delete_tag function
        result = await delete_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_get_images_by_tag_found(self):
        """
        Test retrieving images by a tag.
        """
        expect_result = [self.image]
        tex_tag = self.tag.tag_name
        tag_limit = 10
        tag_offset = 0
        # Mocking the query result to return a list of images
        self.session.query().join().join().filter().order_by().limit().offset().all.return_value = [self.image]
        # Testing the get_images_by_tag function
        result = await get_images_by_tag(tag=tex_tag, limit=tag_limit, offset=tag_offset, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result[0].id, expect_result[0].id)
        self.assertEqual(result[0].image_url, expect_result[0].image_url)
        self.assertEqual(result[0].description, expect_result[0].description)
        self.assertEqual(result[0].user_id, expect_result[0].user_id)

    async def test_get_images_by_tag_not_found(self):
        """
        Test retrieving images by a tag when no images are found.
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        tag_limit = 10
        tag_offset = 0
        # Mocking the query result to return None (no images found)
        self.session.query().join().join().filter().order_by().limit().offset().all.return_value = None
        # Testing the get_images_by_tag function
        result = await get_images_by_tag(tag=tex_tag, limit=tag_limit, offset=tag_offset, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
