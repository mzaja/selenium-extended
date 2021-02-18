from selex import *

# initialize for testing
driver = Driver('Chrome')
driver.get('https://www.google.com')
driver.implicit_wait
driver.find_element_by_text('I agree')
driver.implicit_wait
driver.implicit_wait = 5
driver.implicit_wait = 0
driver.find_elements_by_text('I agree')

e = driver.find_element_by_css_selector("input[title=Search]")
e.send_keys("Python")
e.press.ENTER()

e = driver.find_element_by_text('About')
e.find_element_by_text('About').click()
f = driver.find_element_by_css_selector("div")


# test finding elements by text
driver.find_element_by_text('I agree').click()
driver.find_element_by_text('See more')
driver.find_element_by_text('About')
driver.find_element_by_text('OK').click()
driver.find_element_by_text('learn', True).click()

driver._web_element_cls
driver.create_web_element

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

driver.find_element_by_id()
driver.find_element_by_css_selector()
    
if __name__ == "__main__":
    for browser in SUPPORTED_BROWSERS:
        try:
            d = Driver(browser)
            d.get("https://www.google.com/")
            d.quit()
            print(f"{browser} test completed successfully.")
        except WebDriverException:
            print(f"No driver found for {browser}!")