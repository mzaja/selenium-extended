from selex.updater.firefox import update_geckodriver
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import SessionNotCreatedException

from .const import SUPPORTED_BROWSERS, CHROME, FIREFOX, IE, EDGE
from .keypress import DriverKeyPress
from .updater import update_chromedriver
from .utils import find_elements_by_text, random_wait
from .webelement import WebElement


class Driver(webdriver.Chrome, webdriver.Firefox, webdriver.Ie, webdriver.Edge):
    """
    A custom Selenium webdriver with extended functionality.
    
    Parameters:
        browser (str): Name of the browser to start the webdriver for. Must be one of: ['Chrome', 'Firefox', 'Ie', 'Edge']
        
    Attributes:
        press (KeyPress): Simulates key pressess by calling the appropriately named method e.g. press.ENTER().
        implicit_wait (property): Getting the property returns the current implicit wait time of the webdriver.
                                  Setting the property automatically calls the driver.implicitly_wait() method with the new value.
                                  
    Methods:
        find_element_by_text: Returns the first element with the fully or partially matching textual value. 
        find_elements_by_text: Returns a list of elements with the fully or partially matching textual values.
        type_in: Blindly types in the text into the browser (no particular element selected).
        slow_type: Blindly types the text into the browser with a variable time delay between characters.
    """
    def __init__(self, browser: str, **kwargs):
        browser = browser.capitalize()
        if browser not in SUPPORTED_BROWSERS:
            raise ValueError(f"Browser must be one of: {SUPPORTED_BROWSERS}")
        else:
            try:
                getattr(webdriver, browser).__init__(self, **kwargs)
            except SessionNotCreatedException as caught_exc:
                if browser == CHROME:
                    update_chromedriver(force=False)
                elif browser == FIREFOX:
                    update_geckodriver(force=False)
                else:
                    raise caught_exc
                getattr(webdriver, browser).__init__(self, **kwargs)    # reached only if the exception is not re-raised
        
        self._web_element_cls = WebElement      # return custom WebElement class using this webdriver
        
        self.press = DriverKeyPress(self)       # create interface for simulating key presses
        
        self._implicit_wait = 0                 # sets the default implicit_wait value
    
    @property
    def implicit_wait(self):
        """Returns the duration (in seconds) of the implicit wait webdriver performs when searching for elements."""
        return self._implicit_wait
    
    @implicit_wait.setter
    def implicit_wait(self, value):
        """Automatically changes the implicit wait time of the webdriver whenever a new value is assigned."""
        value = 0 if value < 0 else value
        self.implicitly_wait(value)
        self._implicit_wait = value

    def find_element_by_text(self, text: str, exact_match: bool = False):
        """Finds and returns an element by its text value."""
        return find_elements_by_text(self, True, text, exact_match)
    
    def find_elements_by_text(self, text: str, exact_match: bool = False):
        """Finds and returns elements by their text value."""
        return find_elements_by_text(self, False, text, exact_match)
     
    def type_in(self, string):
        """Types in the provided string into the browser window (to no particular element)."""
        action = ActionChains(self)
        action.send_keys(string)
        action.perform()
        
    def slow_type(self, text: str, max_delay: float = 0.5, min_delay: float = 0.1):
        """Types the text into the browser with a variable delay between characters."""
        for char in text:
            self.type_in(char)
            random_wait(max_delay, min_delay)
