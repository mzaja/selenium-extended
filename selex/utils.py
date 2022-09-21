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
            

def find_elements_by_text(driver, return_one: bool, text: str, exact_match: bool):
    """
    Finds element(s) by their text. 
    A base function for Driver and Element class methods, not to be invoked directly.
    """
    contains_query = f"//*[contains(text(), '{text}')]"
    exact_query = f"//*[text()='{text}']"
    query = exact_query if exact_match == True else contains_query
    method = driver.find_element if return_one == True else driver.find_elements
    return method(By.XPATH, query)