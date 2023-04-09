import unittest

from tests.setup import BaseTestCase
from selex import NoSuchElementException, By


class BaseFindElementsByTextTest:
    """
    Base test case for locating elements by text,
    """
    
    def test_single_no_match(self):
        test_phrase = "Nonexistent text"
        with self.assertRaises(NoSuchElementException):
            self.subject.find_element(By.PARTIAL_TEXT, test_phrase)  
    
    def test_single_match(self):
        test_phrase = "Heading"
        elem = self.subject.find_element(By.PARTIAL_TEXT, test_phrase)
        self.assertIn(test_phrase, elem.text)
    
    def test_single_no_match_exact(self):
        test_phrase = "Heading"
        with self.assertRaises(NoSuchElementException):
            self.subject.find_element(By.TEXT, test_phrase)     
    
    def test_single_match_exact(self):
        test_phrase = "Heading 1"
        elem = self.subject.find_element(By.TEXT, test_phrase)
        self.assertEqual(elem.text, test_phrase)

    def test_multi_no_match(self):
        test_phrase = "Nonexistent text"   
        elems = self.subject.find_elements(By.PARTIAL_TEXT, test_phrase)
        self.assertEqual(len(elems), 0)
    
    def test_multi_match(self):
        test_phrase = "Heading"
        elems = self.subject.find_elements(By.PARTIAL_TEXT, test_phrase)
        self.assertEqual(len(elems), 3)
        for elem in elems:
            self.assertIn(test_phrase, elem.text)
    
    def test_multi_no_match_exact(self):
        test_phrase = "Heading"
        elems = self.subject.find_elements(By.TEXT, test_phrase)
        self.assertEqual(len(elems), 0)
    
    def test_multi_match_exact(self):
        test_phrase = "Heading 1"
        elems = self.subject.find_elements(By.TEXT, test_phrase)
        self.assertEqual(len(elems), 1)
        for elem in elems:
            self.assertEqual(test_phrase, elem.text)
    
    def test_non_text(self):
        """Required to attain 100 % coverage."""
        self.subject.find_elements(By.CSS_SELECTOR, "body")
        # If it does not crash, it passes


class DriverFindElementsByTextTest(BaseTestCase, BaseFindElementsByTextTest):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subject = cls.driver


class ElemFindElementsByTextTest(BaseTestCase, BaseFindElementsByTextTest):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.subject = cls.elem
                

if __name__ == "__main__":
    unittest.main(exit=False)