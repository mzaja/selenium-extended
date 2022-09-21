# import exceptions not used in this package, but very commonly used in projects containing this package
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException

from .driver import get_driver
from .utils import chrome_options
from .wait import wait, wait_factory
from .enums import BrowserType, By