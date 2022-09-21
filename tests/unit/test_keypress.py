import unittest

from tests.setup import BaseTestCase

from selex import By

def test_numpad_nums(self, driver, focus_click: bool):
    """"
    Template function for testing NUMPAD key presses.
    """
    for i in range(0, 10):
        if focus_click == True:
            self.form_field.click()             # focus on the element
        getattr(driver.press, f"NUMPAD{i}")()   # press the key
        self.assertEqual(self.get_field_text(), str(i))  # validate output
        self.form_field.clear()

def test_operators(self, driver, focus_click: bool):
    """"
    Template function for testing operator key presses.
    """
    OPERATOR_KEYS = ["MULTIPLY", "ADD", "SUBTRACT", "DIVIDE", "SEMICOLON", "EQUALS"]
    OPERATORS = "*+-/;="
    
    for i, key in enumerate(OPERATOR_KEYS):
        if focus_click == True:
            self.form_field.click()     # focus on the element
        getattr(driver.press, key)()    # press the key
        self.assertEqual(self.get_field_text(), OPERATORS[i])  # validate output
        self.form_field.clear()

def test_separators(self, driver, focus_click: bool):
    """"
    Template function for testing separator key presses.
    """
    SEPARATOR_KEYS = ["DECIMAL", "SEPARATOR"]
    SEPARATORS = ".,"
    
    if focus_click == True:
        self.form_field.click()     # focus on the element
    for key in SEPARATOR_KEYS:
        getattr(driver.press, key)()
    self.assertIn(self.get_field_text(), [SEPARATORS, SEPARATORS[::-1]])  # equals dot-comma or comma-dot

def test_arrows_bksp_del(self, driver, focus_click: bool):
    """
    Template function for testing arrow keys and backspace/delete.
    Test phrase characters are deleted one by one, using arrow keys to change focus.
    Not the best unit test, but it narrows potential failures down to six keys.
    """
    ARROW_SEQ = ["UP", "RIGHT", "DOWN", "LEFT", ]     # arrow sequence
    BKSP_DEL_SEQ = ["DELETE", "BACKSPACE", "BACKSPACE", "DELETE"]  # del/bksp sequence
    TEST_PHRASE = "1234"
    OUTPUT_SEQ = ["234", "34", "3", ""]
    
    if focus_click == True:
        self.form_field.click()     # focus on the element
    self.form_field.send_keys(TEST_PHRASE)
    self.assertEqual(self.get_field_text(), TEST_PHRASE)    # begin testing
    for i, arrow in enumerate(ARROW_SEQ):
        getattr(driver.press, arrow)()              # press the arrow key
        getattr(driver.press, BKSP_DEL_SEQ[i])()    # press the BKSP/DEL key
        self.assertEqual(self.get_field_text(), OUTPUT_SEQ[i])  # validate the result
    

class KeypressTest(BaseTestCase):
    
    def setUp(self):
        self.form_field = self.driver.find_element(By.ID, "form1")
        self.form_field.clear()
    
    def get_field_text(self):
        return self.driver.execute_script("return arguments[0].value", self.form_field)
    
    def test_driver_numpad_nums(self):
        test_numpad_nums(self, self.driver, focus_click = True)

    def test_elem_numpad_nums(self):
        test_numpad_nums(self, self.form_field, focus_click = False)
    
    def test_driver_operators(self):
        test_operators(self, self.driver, focus_click = True)

    def test_elem_operators(self):
        test_operators(self, self.form_field, focus_click = False)
    
    def test_driver_separators(self):
        test_separators(self, self.driver, focus_click = True)

    def test_elem_separators(self):
        test_separators(self, self.form_field, focus_click = False)  
    
    def test_driver_arrows_bksp_del(self):
        test_arrows_bksp_del(self, self.driver, focus_click = True)
    
    def test_elem_arrows_bksp_del(self):
        test_arrows_bksp_del(self, self.form_field, focus_click = False)
            

if __name__ == "__main__":
    unittest.main(exit=False)