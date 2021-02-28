import logging
import os
import unittest

from collections import namedtuple
from pathlib import Path
from time import sleep

from selex import Driver

TestObjects = namedtuple("SelexObjects", "driver elem")
test_website = os.path.join("resources", "test_website.html")

def test_website_path():
    """"Returns the full path to the test website: Making the testing machine-invariant."""
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_website)
        logging.debug("Test website path obtained from __file__.")
    except NameError:   # if __file__ is not defined
        path = os.path.join(os.getcwd(), "tests", test_website)     # assumes cwd is the selenium-extended repository
        logging.debug("Test website path obtained from cwd.")
    path_uri = Path(path).as_uri()
    logging.debug(path_uri)
    return path_uri
    
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
    driver = test_setup().driver    # ensure the web page opens correctly
    sleep(5)
    driver.quit()