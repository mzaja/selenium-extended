# selenium-extended
 Extends the Selenium webdriver with additional functionality.

## Example usage
### Initialization
```python
from selex import Driver
driver = Driver("Chrome")
driver.get("https://github.com/")
```
### Find element(s) by text
A convenient way is provided to locate elements by the text they contain, bypassing the need to use xpath selectors. Optional parameter **exact_match** controls the strictness of the search.
```python
driver.find_element_by_text("GitHub")  # returns the first element whose text contains the phrase "GitHub"
driver.find_elements_by_text("GitHub")  # returns all elements whose text contains the phrase "GitHub"
driver.find_elements_by_text("GitHub", exact_match = True)  # returns all elements whose text is precisely "GitHub"
```
### Typing and pressing keys
**Driver.press** sub-class emulates key presses without the need to use clunky **ActionChains**. Keys are pressed on a browser level e.g. not directed to any particular element. To send keys to a particular web element, invoke the equivalent **WebElement.press** methods. All keys from `selenium.webdriver.common.keys.Keys` are available.
```python
driver.press.ENTER()  # simulates the ENTER keypress
driver.press.TAB()	 # simulates the TAB keypress
elem = driver.find_element_by_id("form")	 # locate a sample element
elem.press.DELETE()	# press DELETE with the element in focus
```
Longer key press sequences can be emulated using the **type_in** method.
```python
driver.type_in("This text goes to the browser...")
```
More realistic human typing can be simulated using the **slow_type** method. Delays between key presses randomly sampled from the specified time range.
```python
driver.slow_type("I am a human!")  # sent to the browser
elem.slow_type("Typing slowly.", max_delay=1, min_delay=0.3)  # sent to the element with additional parameters
```
### Implicit wait
The **implicit_wait** property simplifies interacting with the webdriver's **implicitly_wait()** mechanic.
```python
current_wait = driver.implicit_wait  # retrieves the current implicit wait time setting
driver.implicit_wait = 5  # sets the implicit wait to 5 seconds
```
The **@wait(time)** decorator can be used to force the user-specified **implicit_wait** time on a class method's execution.
```python
class NewDriver(Driver):
	# __init__ goes here
	@wait(3)
	def search_for_something()
	# do some (soul) searching
new_driver = NewDriver("Chrome")
new_driver.search_for_something()	# waits for 3 seconds before timing out
```
When a custom class has the Selex **Driver** as an attribute (rather than it being a parent class), a custom **@wait(time)** decorator can be manufactures using the **wait_factory** function.
```python
class BankRobbery():
	def __init__(self)
		self.hillary = Driver("Chrome")
	@wait(10)
	def be_useless()
		# die and make Tommy do everything

wait = wait_factory("hillary")  # tells the wait decorator to find the Driver instance at self.hillary
```
### Starting Chrome with a custom profile
Starting Chrome with a custom user profile is made easier by the **chrome_options** method.
```python
from selex import chrome_options
options = chrome_options(user_data_path = PATH, profile_name = "Tanner")  # PATH points to '...\Google\Chrome\User Data'
driver = Driver("Chrome", options=options)  # starts Chromedriver using the custom profile
```
