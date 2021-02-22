import time
import unittest

from tests.setup import BaseTestCase
from selex import *

wait_dec = wait_factory("driver")   # create a wait_dec deocrator for a driver available as a self.driver attribute
tolerance = 0.2     # tolerance for assertions in time tests (in seconds)

class DriverImplicitWaitTest(BaseTestCase):
    
    def test_setting_and_getting(self):
        self.driver.implicit_wait = 5
        self.assertEqual(self.driver.implicit_wait, 5)
    
    def test_performance(self):
        try:
            for t_wait in [0, 2]:
                self.driver.implicit_wait = t_wait
                t1 = time.time()
                try:
                    self.driver.find_element_by_id("No such id exists")
                except NoSuchElementException:
                    pass
                test_time = time.time() - t1
                self.assertBetween(test_time, t_wait - tolerance, t_wait + tolerance)
        finally:
            self.driver.implicit_wait = 0

    @wait_dec(1)
    def test_decorator(self):
        self.assertEqual(self.driver.implicit_wait, 1)   # a faster way of testing the decorator works without waiting


if __name__ == "__main__":
    unittest.main(exit=False)