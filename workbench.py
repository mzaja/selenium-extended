from selex import *

# initialize for testing
driver = Driver('Chrome')
driver.get('https://www.google.com')

# key press test
driver.press.keys
driver.press.ENTER
driver.press.ENTER()

# test implicit wait getter and setter
driver.implicit_wait = 5    # setter
driver.implicit_wait        # getter
driver.find_element_by_id("surely no such element exists")      # takes 5 seconds
driver.implicit_wait = 0
driver.implicit_wait
driver.find_element_by_id("surely no such element exists")      # takes 0 seconds

    
if __name__ == "__main__":
    for browser in SUPPORTED_BROWSERS:
        try:
            d = Driver(browser)
            d.get("https://www.google.com/")
            d.quit()
            print(f"{browser} test completed successfully.")
        except WebDriverException:
            print(f"No driver found for {browser}!")