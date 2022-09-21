import time
import unittest

from tests.setup import BaseTestCase
from selex import *

wait_dec = wait_factory("driver")   # create a wait_dec deocrator for a driver available as a self.driver attribute
TOLERANCE = 0.2     # tolerance for assertions in time tests (in seconds)
TEST_WAIT = 1       # test wait time

class DriverImplicitWaitFactoryTest(BaseTestCase):
    
    def test_setting_and_getting(self):
        self.driver.implicit_wait = 5
        self.assertEqual(self.driver.implicit_wait, 5)
    
    def test_performance(self):
        try:
            for t_wait in [0, 2]:
                self.driver.implicit_wait = t_wait
                t1 = time.time()
                try:
                    self.driver.find_element(By.ID, "No such id exists")
                except NoSuchElementException:
                    pass
                test_time = time.time() - t1
                self.assertBetween(test_time, t_wait - TOLERANCE, t_wait + TOLERANCE)
        finally:
            self.driver.implicit_wait = 0

    @wait_dec(TEST_WAIT)
    def test_decorator(self):
        self.assertEqual(self.driver.implicit_wait, TEST_WAIT)   # a faster way of testing the decorator works without waiting


class DriverImplicitWaitTest(unittest.TestCase):
    """Tests the standalone @wait decorator in a child class of Driver."""
    
    class TestDriver(type(get_driver(BrowserType.CHROME))):
        @wait(TEST_WAIT)    
        def search_for_nothing(self):
            self.find_element(By.ID, "Nonexistent id")
    
    def test_decorator(self):
        driver = self.TestDriver(BrowserType.CHROME)
        t1 = time.time()
        try:
            driver.search_for_nothing()
        except NoSuchElementException:
            pass
        test_time = time.time() - t1
        try: # assert between (self.assertBetween() is not available because this test does not inherit from the BaseTest class)
            self.assertGreater(test_time, TEST_WAIT - TOLERANCE)
            self.assertLess(test_time, TEST_WAIT + TOLERANCE)
        finally:
            driver.quit()   # important not to forget this


if __name__ == "__main__":
    unittest.main(exit=False)