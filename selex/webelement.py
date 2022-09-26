import os
from typing import List

from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.webdriver.remote.webelement import WebElement as BaseWebElement

from .enums import By
from .keypress import ElemKeyPress
from .utils import find_element_by_text, find_elements_by_text, random_wait


class WebElement(BaseWebElement):
    """
    A custom WebElement class returned by the custom Selenium webdriver. 
    Returned by the Driver class and should not be instantiated directly.
    
    Attributes:
        press (KeyPress): Simulates key pressess by calling the appropriately named method e.g. press.ENTER().
                          Keys are sent into the element (rather than the browser itself as with the Driver class).
    
    Methods:
        find_element_by_text: Returns the first sub-element with the fully or partially matching textual value. 
        find_elements_by_text: Returns a list of sub-elements with the fully or partially matching textual values.
        slow_type: Types the text into the element with a variable time delay between characters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.press = ElemKeyPress(self)
    
    def find_ancestor(self, level: int = 1, recursive: bool = True):
        """
        Returns the n-th ancestor of the current web element.
        
        Parameters:
            level (int): Generation of the ancestor element to be returned (1: parent, 2: grandparent etc.)
            recursive (bool): If True, the ancestor element is searched for recursively. 
                              If level exceeds the number of ancestors, the last ancestor is returned.
                              if False, the search is faster but a NoSuchElement exception is raised on a nonexistant ancestor.
        """
        err_msg_neg_non_int = "Parameter 'level' must be a non-negative integer."
        if type(level) != int:
            raise TypeError(err_msg_neg_non_int)
        if level < 0:
            raise ValueError(err_msg_neg_non_int)
        if level == 0:
            return self
        if level > 0:
            if recursive == True:
                try:
                    parent = self.find_element(By.XPATH, "..")
                    return parent.find_ancestor(level - 1, recursive=True)
                except InvalidSelectorException:
                    return self
            else: # if recursive == False
                try:
                    return self.find_element(By.XPATH, ".." + (level-1) * "/..")
                except (InvalidSelectorException, NoSuchElementException):
                    raise NoSuchElementException("No such element exists because the document boundaries have been exceeded.")
    
    
    def find_element(self, by: By.ID, value: str = None) -> "WebElement":
        """Finds and returns an element by its text value."""
        if by is By.TEXT:
            return find_element_by_text(self._parent, value, True)
        elif by is By.PARTIAL_TEXT:
            return find_element_by_text(self._parent, value, False)
        else:
            return super().find_element(by, value)
        
    def find_elements(self, by: By.ID, value: str = None) -> List["WebElement"]:
        """Finds and returns elements by their text value."""
        if by is By.TEXT:
            return find_elements_by_text(self._parent, value, True)
        elif by is By.PARTIAL_TEXT:
            return find_elements_by_text(self._parent, value, False)
        else:
            return super().find_elements(by, value)

    def save_as_png(self, output_file: str):
        """Saves the web element as a PNG image. 'output_file' does not need to include the .png extension."""     
        if os.path.splitext(output_file)[1] == '':   # append .png extension if none exists
            output_file += '.png'   
        with open(output_file,"wb") as f:  # save the element screenshot as .png
            f.write(self.screenshot_as_png)

    def slow_type(self, text: str, max_delay: float = 0.5, auto_clear: bool = True, min_delay: float = 0.1):
        """Types the text into this element with a variable delay between characters."""
        if auto_clear == True:
            self.clear()
        for char in text:
            self.send_keys(char)
            random_wait(max_delay, min_delay)