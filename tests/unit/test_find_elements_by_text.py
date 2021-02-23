import unittest

from tests.setup import BaseTestCase
from selex import *


def single_no_match(self, driver):
    test_phrase = "Nonexistent text"
    with self.assertRaises(NoSuchElementException):
        elem = driver.find_element_by_text(test_phrase, exact_match=False)      

def single_match(self, driver):
    test_phrase = "Heading"
    elem = driver.find_element_by_text(test_phrase, exact_match=False)
    self.assertIn(test_phrase, elem.text)

def single_no_match_exact(self, driver):
    test_phrase = "Heading"
    with self.assertRaises(NoSuchElementException):
        elem = driver.find_element_by_text(test_phrase, exact_match=True)      

def single_match_exact(self, driver):
    test_phrase = "Heading 1"
    elem = driver.find_element_by_text(test_phrase, exact_match=True)
    self.assertEqual(elem.text, test_phrase)


def multi_no_match(self, driver):
    test_phrase = "Nonexistent text"   
    elems = driver.find_elements_by_text(test_phrase, exact_match=False)
    self.assertEqual(len(elems), 0)

def multi_match(self, driver):
    test_phrase = "Heading"
    elems = driver.find_elements_by_text(test_phrase, exact_match=False)
    self.assertEqual(len(elems), 3)
    for elem in elems:
        self.assertIn(test_phrase, elem.text)

def multi_no_match_exact(self, driver):
    test_phrase = "Heading"
    elems = driver.find_elements_by_text(test_phrase, exact_match=True)
    self.assertEqual(len(elems), 0)

def multi_match_exact(self, driver):
    test_phrase = "Heading 1"
    elems = driver.find_elements_by_text(test_phrase, exact_match=True)
    self.assertEqual(len(elems), 1)
    for elem in elems:
        self.assertEqual(test_phrase, elem.text)


class DriverFindElementsByTextTest(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subject = cls.driver
    
    def test_single_no_match(self):
        single_no_match(self, self.subject)
    
    def test_single_match(self):
        single_match(self, self.subject)
    
    def test_single_no_match_exact(self):
        single_no_match(self, self.subject)
    
    def test_single_match_exact(self):
        single_match(self, self.subject)

    def test_multi_no_match(self):
        multi_no_match(self, self.subject)
    
    def test_multi_match(self):
        multi_match(self, self.subject)
    
    def test_multi_no_match_exact(self):
        multi_no_match(self, self.subject)
    
    def test_multi_match_exact(self):
        multi_match(self, self.subject)


class ElemFindElementsByTextTest(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subject = cls.elem
    
    def test_single_no_match(self):
        single_no_match(self, self.subject)
    
    def test_single_match(self):
        single_match(self, self.subject)
    
    def test_single_no_match_exact(self):
        single_no_match(self, self.subject)
    
    def test_single_match_exact(self):
        single_match(self, self.subject)

    def test_multi_no_match(self):
        multi_no_match(self, self.subject)
    
    def test_multi_match(self):
        multi_match(self, self.subject)
    
    def test_multi_no_match_exact(self):
        multi_no_match(self, self.subject)
    
    def test_multi_match_exact(self):
        multi_match(self, self.subject)
            

if __name__ == "__main__":
    unittest.main(exit=False)