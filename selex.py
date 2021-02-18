from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

SUPPORTED_BROWSERS = ['Chrome', 'Firefox', 'Ie', 'Edge']

class Driver(webdriver.Chrome, webdriver.Firefox, webdriver.Ie, webdriver.Edge):
    """
    A custom Selenium webdriver with extended functionality.
    """
    def __init__(self, browser: str):
        browser = browser.capitalize()
        if browser not in SUPPORTED_BROWSERS:
            raise TypeError(f"Browser must be one of: {SUPPORTED_BROWSERS}")
        else:
            getattr(webdriver, browser).__init__(self)
        
        self._web_element_cls = Element     # return custom WebElement class using this webdriver
        self.press = DriverKeyPress(self)
        self._implicit_wait = 0
    
    @property
    def implicit_wait(self):
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
    

class Element(WebElement):
    """
    A custom WebElement class returned by the custom Selenium webdriver.
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


class BaseKeyPress:
    """
    Base KeyPress class. 
    Allows creation of two separate KeyPress classes, one for the driver and ther other for web elements.
    """
    def __init__(self):
        self.keys = tuple(x for x in dir(Keys) if not x.startswith('__'))


class DriverKeyPress(BaseKeyPress):
    """
    Simulates key presses in a simple and convenient way. 
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


class ElemKeyPress(BaseKeyPress):
    """
    Simulates key presses in a simple and convenient way. 
    """
    def __init__(self, element):
        super().__init__()
        self._element = element
        for key_name in self.keys:
            setattr(self, key_name, lambda x=getattr(Keys, key_name): self._element.send_keys(x))
            

def find_elements_by_text(driver: Driver, return_one: bool, text: str, exact_match: bool):
    """Finds element(s) by their text. A base function for Driver and Element class methods"""
    contains_query = f"//*[contains(text(), '{text}')]"
    exact_query = f"//*[text()='{text}']"
    query = exact_query if exact_match == True else contains_query
    method = driver.find_element_by_xpath if return_one == True else driver.find_elements_by_xpath
    return method(query)


def wait(time: float): 
    """
    Intended to be used as a decorator within the Driver class. 
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
            self.implicit_wait = new_wait
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
        Intended to be used as a decorator within the Driver class. 
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
                getattr(self, driver_attr_name).implicit_wait = new_wait
                try:
                    return method(self, *args, **kwargs)
                finally:
                    getattr(self, driver_attr_name).implicit_wait = old_wait
            return wrapper
        return decorator
    return wait