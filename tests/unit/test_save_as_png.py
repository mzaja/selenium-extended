import os
import unittest

from PIL import Image

from tests.setup import BaseTestCase
from selex import *

def remove_image(image_name: str):
    try:
        os.remove(image_name)
    except FileNotFoundError:
        pass

def compare_images(img1: str, img2: str):
    try:
        obj1 = Image.open(img1)
        obj2 = Image.open(img2)
        return obj1 == obj2
    finally:
        obj1.close()
        obj2.close()

test_image = os.path.join("tests", "resources", "image1.png")
saved_image = os.path.join("tests", "resources", "saved_image.png")

class ElemSaveAsPngTest(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.image_elem = cls.driver.find_element(By.CSS_SELECTOR, "img")     # find image in DOM

    def setUp(self):
        remove_image(saved_image)

    def tearDown(self):
        remove_image(saved_image)

    def test_save_as_png(self):
        self.image_elem.save_as_png(saved_image)
        self.assertTrue(compare_images(saved_image, test_image))

    def test_save_without_extension(self):
        self.image_elem.save_as_png(os.path.splitext(saved_image)[0])   # save without .png extension
        self.assertTrue(compare_images(saved_image, test_image))


if __name__ == "__main__":
    unittest.main(exit=False)
