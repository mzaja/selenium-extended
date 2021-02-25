import unittest

from tests.setup import BaseTestCase
from selex import *

LEVELS = ['label', 'form', 'body', 'html']

def match_found(self, recursive: bool):
    for i in range(0, 4):
        tag = self.elem.find_ancestor(level = i, recursive = recursive).tag_name
        self.assertEqual(tag, LEVELS[i])

def out_of_bounds(self, recursive: bool):
    for i in [4, 99]:
        if recursive == True:
            tag = self.elem.find_ancestor(level = i, recursive = recursive).tag_name
            self.assertEqual(tag, LEVELS[-1])
        elif recursive == False:
            with self.assertRaises(NoSuchElementException):
                tag = self.elem.find_ancestor(level = i, recursive = recursive).tag_name


class ElemFindAncestorTest(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.elem = cls.driver.find_element_by_css_selector("label")
    
    def test_type_error(self):
        for arg in [2.3, 'str', False]:
            with self.assertRaises(TypeError):
                self.elem.find_ancestor(level=arg)
                
    def test_value_error(self):
        with self.assertRaises(ValueError):
            self.elem.find_ancestor(level = -1)

    def test_recursive_find(self):
        match_found(self, recursive=True)
    
    def test_non_recursive(self):
        match_found(self, recursive=False)
        
    def test_recursive_out_of_bounds(self):
        out_of_bounds(self, recursive=True)
    
    def test_non_recursive_out_of_bounds(self):
        out_of_bounds(self, recursive=False)
  
            
if __name__ == "__main__":
    unittest.main(exit=False)