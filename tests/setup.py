import os
from collections import namedtuple
import unittest

from selex import Driver

# driver, _ = test_setup()

TestObjects = namedtuple("SelexObjects", "driver elem")

def test_website_path():
    """"Returns the full path to the test website: Making the testing machine-invariant."""
    test_website = "test_website.html"
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_website)
    except NameError:   # if __file__ is not defined
        path = os.path.join(os.getcwd(), "tests", test_website)
    return path
    
def test_setup():
    """
    Initializes the webdriver, opens the test website and returns a (driver, webelement) tuple for test purposes.
    """
    driver = Driver("Chrome")
    driver.get(test_website_path())
    webelem = driver.find_element_by_css_selector("html")  # store the whole webpage as an element
    return TestObjects(driver, webelem)

class BaseTestCase(unittest.TestCase):
    """Base test class with defined driver and web element setup and cleanup actions."""
    
    @classmethod
    def setUpClass(cls):
        cls.driver, cls.elem = test_setup()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        
    def assertBetween(self, value: float, lower_limit: float, upper_limit: float, inclusive: bool = False):
        if inclusive == False:
            self.assertGreater(value, lower_limit)
            self.assertLess(value, upper_limit)
        elif inclusive == True:
            self.assertGreaterEqual(value, lower_limit)
            self.assertLessEqual(value, upper_limit)
            

if __name__ == "__main__":
    pass