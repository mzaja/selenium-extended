import unittest
from functools import partial

from tests.setup import test_setup
from selex import *

driver, webelem = test_setup()  # initialize the webdriver and create a test webelement object
          

def test_find_element_by_text(self, driver):
    """
    Tests the 'find_element_by_text' method. Param 'driver' can be either a webdriver or a webelement object.
    """       
    test_phrase = "Nonexistent text"    # initial test phrase
    
    with self.assertRaises(NoSuchElementException):     # test raising an exception on no match
        elem = driver.find_element_by_text(test_phrase)  
    
    test_phrase = "Heading"     # new test phrase

    elem = driver.find_element_by_text(test_phrase)     # test finding a non-exact match
    assert test_phrase in elem.text
    
    with self.assertRaises(NoSuchElementException):     # test raising an exception on no matches
        elem = driver.find_element_by_text(test_phrase, exact_match=True)  

    test_phrase = "Heading 1"       # new test phrase
    
    elem = driver.find_element_by_text(test_phrase, exact_match=True)   # test finding an exact match
    assert test_phrase == elem.text
    

def test_find_elements_by_text(self, driver):
    """
    Tests the 'find_elements_by_text' method. Param 'driver' can be either a webdriver or a webelement object.
    """
    test_phrase = "Nonexistent text"    # initial test phrase
    
    elems = driver.find_elements_by_text(test_phrase)   # test non-existent, non-exact matches
    assert len(elems) == 0
    
    test_phrase = "Heading"     # new test phrase
    
    elems = driver.find_elements_by_text(test_phrase)   # test non-exact matches
    assert len(elems) == 3
    for elem in elems:
        assert test_phrase in elem.text

    elems = driver.find_elements_by_text(test_phrase, exact_match=True)   # test non-exact matches
    assert len(elems) == 0
    
    test_phrase = "Heading 1"     # new test phrase
    
    elems = driver.find_elements_by_text(test_phrase)   # test non-exact matches
    assert len(elems) == 1
    for elem in elems:
        assert test_phrase in elem.text


class DriverTest(unittest.TestCase):
    
    def test_find_element_by_text(self):
        test_find_element_by_text(self, driver)
        
    def test_find_elements_by_text(self):
        test_find_elements_by_text(self, driver)


class ElemTest(unittest.TestCase):
    
    def test_find_element_by_text(self):
        test_find_element_by_text(self, webelem)
        
    def test_find_elements_by_text(self):
        test_find_elements_by_text(self, webelem)
            

if __name__ == "__main__":
    try:
        unittest.main(exit=False)
    finally:
        driver.quit()