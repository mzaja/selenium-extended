import random
import time

from selenium.webdriver.chrome.options import Options as ChromeOptions

from selex.enums import By

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


def make_text_search_query(text: str, exact_match: bool):
    """Generates the xpath search query that finds the specified text in the webpage."""
    return f"//*[text()='{text}']" if exact_match is True else f"//*[contains(text(), '{text}')]"

def find_element_by_text(driver, text: str, exact_match: bool):
    """
    Finds element(s) by their text. 
    A base function for Driver and Element class methods, not to be invoked directly.
    """
    return driver.find_element(By.XPATH, make_text_search_query(text, exact_match))

def find_elements_by_text(driver, text: str, exact_match: bool):
    """
    Finds element(s) by their text. 
    A base function for Driver and Element class methods, not to be invoked directly.
    """
    return driver.find_elements(By.XPATH, make_text_search_query(text, exact_match))