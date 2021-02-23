from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class KeyPress:
    """
    Base KeyPress class. 
    Allows creation of two separate KeyPress classes, one for the driver and the other one for web elements.
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