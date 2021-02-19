import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement as BaseWebElement

SUPPORTED_BROWSERS = ['Chrome', 'Firefox', 'Ie', 'Edge']

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
    def __init__(self, browser: str):
        browser = browser.capitalize()
        if browser not in SUPPORTED_BROWSERS:
            raise TypeError(f"Browser must be one of: {SUPPORTED_BROWSERS}")
        else:
            getattr(webdriver, browser).__init__(self)
        
        self._web_element_cls = WebElement      # return custom WebElement class using this webdriver
        
        self.press = DriverKeyPress(self)       # 
        
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

    def slow_type(self, text: str, max_delay: float = 0.5, auto_clear: bool = True, min_delay: float = 0.1):
        """Types the text into this element with a variable delay between characters."""
        if auto_clear == True:
            self.clear()
        for char in text:
            self.send_keys(char)
            random_wait(max_delay, min_delay)


class KeyPress:
    """
    Base KeyPress class. 
    Allows creation of two separate KeyPress classes, one for the driver and ther other for web elements.
    """
    def __init__(self):
        self.keys = tuple(x for x in dir(Keys) if not x.startswith('__'))


class DriverKeyPress(KeyPress):
    """
    Simulates key presses in a simple and convenient way, e.g. driver.press.ENTER().
    Keys are sent into the browser without focus on any particuar element.
    """
    def __init__(self, driver):
        super().__init__()
        self._driver = driver
        for key_name in self.keys:
            # have key press available as attribute (property) e.g. press.ENTER
            #setattr(self.__class__, key_name, property(fget=lambda self, x=getattr(Keys, key_name): self._press_key(x)))
            # have key press available as function e.g. press.ENTER() 
            setattr(self, key_name, lambda x=getattr(Keys, key_name): self._press_key(x))
            
    def _press_key(self, key):
        """Base method for pressing keys. Used to derive convenience methods rather than be used directly."""
        action = ActionChains(self._driver)
        action.send_keys(key)
        action.perform()


class ElemKeyPress(KeyPress):
    """
    Simulates key presses in a simple and convenient way, e.g. element.press.ENTER().
    Keys are sent into a particuar web element.
    """
    def __init__(self, element):
        super().__init__()
        self._element = element
        for key_name in self.keys:
            setattr(self, key_name, lambda x=getattr(Keys, key_name): self._element.send_keys(x))


def chrome_options(user_data_path: str, profile_name: str = 'Default'):
    """Returns the webdriver Chrome options for the provided user data path and profile name."""
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_path}")
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--disable-blink-features=AutomationControlled")   # mentioned on stack exchange
    return options


def random_wait(max_wait: float, min_wait: float = 0):
    """Waits for a random time between min_wait and max_wait."""
    time.sleep(random.uniform(min_wait, max_wait))
            

def find_elements_by_text(driver: Driver, return_one: bool, text: str, exact_match: bool):
    """
    Finds element(s) by their text. 
    A base function for Driver and Element class methods, not to be invoked directly.
    """
    contains_query = f"//*[contains(text(), '{text}')]"
    exact_query = f"//*[text()='{text}']"
    query = exact_query if exact_match == True else contains_query
    method = driver.find_element_by_xpath if return_one == True else driver.find_elements_by_xpath
    return method(query)


def wait(time: float): 
    """
    Intended for use as a decorator within the Driver class. 
    Forces the implicit wait on executing the class methods.
    Example:
        @wait(5)
        def method(self, *args, **kwargs)
        ->
        method is executed with an implicit webdriver wait of 5 seconds.
    """
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            old_wait = self.implicit_wait
            self.implicit_wait = time
            try:
                return method(self, *args, **kwargs)
            finally:
                self.implicit_wait = old_wait
        return wrapper
    return decorator


def wait_factory(driver_attr_name: str):
    """
    Returns a wait decorator for a webdriver class atribute named driver_attr_name.
    Example:
        wait = wait_factory("driver")
        
        class HasDriverAsAttribute:
            def __init__(self):
                self.driver = Driver("Chrome")
            
            @wait(5)
            def method(self, *args, **kwargs):
                <Does something with self.driver>
        
        -> method is executed with an implicit webdriver wait of 5 seconds
    """
    def wait(time: float): 
        """
        Intended for use as a decorator within the Driver class. 
        Forces the implicit wait on executing the class methods.
        Example:
            @wait(5)
            def method(self, *args, **kwargs)
            ->
            method is executed with an implicit webdriver wait of 5 seconds.
        """
        def decorator(method):
            def wrapper(self, *args, **kwargs):
                old_wait = getattr(self, driver_attr_name).implicit_wait
                getattr(self, driver_attr_name).implicit_wait = time
                try:
                    return method(self, *args, **kwargs)
                finally:
                    getattr(self, driver_attr_name).implicit_wait = old_wait
            return wrapper
        return decorator
    return wait