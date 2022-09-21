from enum import Enum

from selenium.webdriver.common.by import By as _BaseBy

class BrowserType(Enum):
    CHROME = "Chrome"
    FIREFOX = "Firefox"
    IE = "Ie"
    EDGE = "Edge"

# Technically not an Enum, but is used like one
class By(_BaseBy):
    TEXT = "text"
    PARTIAL_TEXT = "partial text"