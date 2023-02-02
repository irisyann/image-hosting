import os
import unittest
from flask import Flask
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

from app import app, generate_filename, valid_file


class TestApp(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_valid_file(self):
        self.assertTrue(valid_file("image.jpg"))
        self.assertTrue(valid_file("image.jpeg"))
        self.assertTrue(valid_file("image.png"))
        self.assertTrue(valid_file("image.gif"))
        self.assertFalse(valid_file("image.txt"))
        self.assertFalse(valid_file(""))

    def test_generate_filename(self):
        filename = generate_filename("test.jpg")
        self.assertTrue(filename.startswith(""))
        self.assertTrue(filename.endswith("test.jpg"))

    def test_upload_image_file(self):
        with open("test.jpg", "wb") as fp:
            fp.write(b"image_file_data")
            fp.close()

        with open("test.jpg", "rb") as fp:
            file = FileStorage(fp, filename="test.jpg", content_type="image/jpeg")

            with self.client:
                response = self.client.post("/result", data={"file": file})
                self.assertEqual(response.status_code, 200)
                fp.close()
                os.remove("test.jpg")

    def test_upload_invalid_file(self):
        with open("test.txt", "wb") as fp:
            fp.write(b"invalid_file_data")
            fp.close()

        with open("test.txt", "rb") as fp:
            file = FileStorage(fp, filename="test.txt", content_type="text/plain")
            response = self.client.post("/result", data={"file": file})
            self.assertEqual(response.status_code, 500)
            fp.close()
            os.remove("test.txt")

    def test_upload_no_file(self):
        response = self.client.post("/result", data={})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
    app.run()
