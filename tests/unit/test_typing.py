import time
import unittest

from tests.setup import BaseTestCase
from selex import *

min_max_delay = (0.1, 0.15)
tolerance = 0.2


class TypingTest(BaseTestCase):
    
    def setUp(self):
        self.form_field = self.driver.find_element_by_id("form1")
        self.form_field.clear()
    
    def get_field_text(self):
        return self.driver.execute_script("return arguments[0].value", self.form_field)
    
    def test_elem_slow_type(self):
        """
        Tests slowly typing the test phrase into a web element.
        """
        test_phrase = "Dr1v3r"
        
        t1 = time.time()
        self.form_field.slow_type(text = test_phrase, max_delay = min_max_delay[1], auto_clear = False, min_delay = min_max_delay[0])
        time_taken = time.time() - t1
        
        self.assertEqual(self.get_field_text(), test_phrase)     # assert the correct phrase has been typed in
        
        lower_limit = len(test_phrase)*min_max_delay[0] - tolerance
        upper_limit = len(test_phrase)*min_max_delay[1] + tolerance
        self.assertBetween(time_taken, lower_limit=lower_limit, upper_limit=upper_limit)  # asses time duration
    
    
    def test_elem_slow_type_clear(self):
        """
        Tests that the web element is cleared before typing if auto_clear = True.
        """
        test_phrase = "Dr1v3r"
        self.form_field.send_keys(test_phrase)
        self.form_field.slow_type(text = test_phrase, max_delay = 0, auto_clear = True, min_delay = 0)
        self.assertEqual(self.get_field_text(), test_phrase)
        
        
    def test_driver_slow_type(self):
        """
        Tests slowly typing into the browser, with the last interacted element being in focus.
        """
        test_phrase = "Tanner"
        
        self.form_field.click()     # set focus on the form field
        t1 = time.time()
        self.driver.slow_type(text = test_phrase, max_delay = min_max_delay[1], min_delay = min_max_delay[0])
        time_taken = time.time() - t1
        
        self.assertEqual(self.get_field_text(), test_phrase)     # assert the correct phrase has been typed in
        
        lower_limit = len(test_phrase)*min_max_delay[0] - tolerance
        upper_limit = len(test_phrase)*min_max_delay[1] + tolerance
        self.assertBetween(time_taken, lower_limit=lower_limit, upper_limit=upper_limit)  # asses time duration
    
    
    def test_driver_slow_type_no_focus(self):
        """
        Tests that the text is typed on browser level, by sending keys to a non-input element.
        """
        test_phrase = "John"
        self.driver.find_element_by_css_selector("h1").click()    # focus on a non-input element    
        self.driver.slow_type(test_phrase, max_delay = min_max_delay[1], min_delay = min_max_delay[0])
        self.assertEqual(self.get_field_text(), '')
      
        
    def test_driver_type_in(self):
        """
        Tests quickly typing the text into the browser.
        """
        test_phrase = "Tanner"
        self.form_field.click()     # set focus on the form field
        self.driver.type_in(test_phrase)
        self.assertEqual(self.get_field_text(), test_phrase)
      
        
    def test_driver_type_in_no_focus(self):
        """
        Tests that the text is typed on browser level, by sending keys to a non-input element.
        """
        test_phrase = "John"
        self.driver.find_element_by_css_selector("h1").click()    # focus on a non-input element    
        self.driver.type_in(test_phrase)
        self.assertEqual(self.get_field_text(), '')


if __name__ == "__main__":
    unittest.main(exit=False)