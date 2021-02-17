from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

SUPPORTED_BROWSERS = ['Chrome', 'Firefox', 'Ie', 'Edge']

class Driver(webdriver.Chrome, webdriver.Firefox, webdriver.Ie, webdriver.Edge):
    """
    doc
    """
    def __init__(self, browser: str):
        browser = browser.capitalize()
        if browser not in SUPPORTED_BROWSERS:
            raise TypeError(f"Browser must be one of: {SUPPORTED_BROWSERS}")
        else:
            getattr(webdriver, browser).__init__(self)
        
        self.press = KeyPress(self)
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


class KeyPress:
    """
    doc
    """
    def __init__(self, driver):
        self._driver = driver
        self.keys = tuple(x for x in dir(Keys) if not x.startswith('__'))
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
        
        
def wait(enable: bool = True):      # work in progress -> create a @wait(t) decorator
    """
    Decorator with parameter 'enable': 
        If True: Apply implicit wait to the nominated class method. 
        if False: Do not apply implicit wait to the nominated class method.
    
    Selenium webdriver must be available as an attribute at 'self._driver'.
    Default implicit wait must be attribute at 'self._implicit_wait'.
    """
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            default_wait = self._implicit_wait
            temporary_wait = IMPLICIT_WAIT if enable == True else 0
            self._driver.implicitly_wait(temporary_wait)
            retval = method(self, *args, **kwargs)
            self._driver.implicitly_wait(default_wait)
            return retval
        return wrapper
    return decorator