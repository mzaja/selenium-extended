from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

SUPPORTED_BROWSERS = ['Chrome', 'Firefox', 'Ie']

class Driver(webdriver.Chrome, webdriver.Firefox, webdriver.Ie):
    """doc"""
    def __init__(self, browser: str):
        browser = browser.capitalize()
        if browser not in SUPPORTED_BROWSERS:
            raise TypeError(f"Browser must be one of: {SUPPORTED_BROWSERS}")
        else:
            getattr(webdriver, browser).__init__(self)


for browser in SUPPORTED_BROWSERS:
    try:
        d = Driver(browser)
        d.get("https://www.google.com/")
        d.quit()
        print(f"{browser} test completed successfully.")
    except WebDriverException:
        print(f"No driver found for {browser}!")