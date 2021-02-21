import os

from selex import Driver

def test_website_path():
    """"Returns the full path to the test website: Making the testing machine-invariant."""
    test_website = "test_website.html"
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_website)
    except NameError:   # if __file__ is not defined
        path = os.path.join(os.getcwd(), "tests", test_website)
    return path
    
def test_setup():
    """
    Initializes the webdriver, opens the test website and returns a test webelement.
    """
    driver = Driver("Chrome")
    driver.get(test_website_path())
    webelem = driver.find_element_by_css_selector("html")  # store the whole webpage as an element
    return driver, webelem
    
if __name__ == "__main__":
    test_setup()