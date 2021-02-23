import os

from selenium.webdriver.remote.webelement import WebElement as BaseWebElement

from .keypress import ElemKeyPress
from .utils import find_elements_by_text, random_wait


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
    
    def find_element_by_text(self, text: str, exact_match: bool = False):
        """Finds and returns an element by its text value."""
        return find_elements_by_text(self._parent, True, text, exact_match)
    
    def find_elements_by_text(self, text: str, exact_match: bool = False):
        """Finds and returns elements by their text value."""
        return find_elements_by_text(self._parent, False, text, exact_match)

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