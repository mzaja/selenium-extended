import time
import unittest

from tests.setup import test_setup
from selex import *

driver, webelem = test_setup()  # initialize the webdriver and create a test webelement object

wait_dec = wait_factory("driver_attr")   # create a wait_dec deocrator for a driver located at self.driver_attr
tolerance = 0.2     # tolerance for assertions in time tests (in seconds)

class DriverImplicitWaitTest(unittest.TestCase):
    
    def setUp(self):
        self.driver_attr = driver
    
    def test_setting_and_getting(self):
        driver.implicit_wait = 5
        self.assertEqual(driver.implicit_wait, 5)
    
    def test_performance(self):
        try:
            for t_wait in [0, 2]:
                driver.implicit_wait = t_wait
                t1 = time.time()
                try:
                    driver.find_element_by_id("No such id exists")
                except NoSuchElementException:
                    pass
                test_time = time.time() - t1
                self.assertGreaterEqual(test_time, t_wait - tolerance)  # assert test time within tolerance from t_wait
                self.assertLessEqual(test_time, t_wait + tolerance)
        finally:
            driver.implicit_wait = 0

    @wait_dec(1)
    def test_decorator(self):
        self.assertEqual(self.driver_attr.implicit_wait, 1)   # a faster way of testing the decorator works without waiting


if __name__ == "__main__":
    try:
        unittest.main(exit=False)
    finally:
        driver.quit()