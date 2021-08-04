import unittest
from unittest.mock import patch, ANY, call

from selenium.common.exceptions import SessionNotCreatedException

from selex import Driver, chrome_options
from selex.const import SUPPORTED_BROWSERS, CHROME, FIREFOX, IE, EDGE

USER_DATA_PATH = "dummy/user/data/path"
USER_PROFILE = "Profile 99"
KWARGS = {'kw1': 3, 'kw2': 'Whatever'}


class DriverInitTest(unittest.TestCase):
    """
    Tests the initialization of the Driver class.
    """
    
    @patch("selenium.webdriver.Edge.__init__")
    @patch("selenium.webdriver.Ie.__init__")
    @patch("selenium.webdriver.Firefox.__init__")
    @patch("selenium.webdriver.Chrome.__init__")
    def test_correct_browser_choice(self, mock_chrome, mock_firefox, mock_ie, mock_edge):
        for browser, mock in zip(SUPPORTED_BROWSERS, [mock_chrome, mock_firefox, mock_ie, mock_edge]):
            with self.subTest(browser):
                Driver(browser, **KWARGS)
                mock.assert_called_once_with(ANY, **KWARGS)
    
    def test_wrong_browser_choice(self):
        with self.assertRaises(ValueError):
            Driver("No such browser!")

    @patch("selex.driver.update_chromedriver")  # must patch in selex.driver namespace because update_chromedriver is imported there
    @patch("selenium.webdriver.Chrome.__init__")
    def test_chrome_driver_mismatch(self, mock_browser, mock_updater):
        mock_browser.side_effect = [SessionNotCreatedException, None]
        Driver(CHROME, **KWARGS)
        mock_browser.assert_has_calls([call(ANY, **KWARGS)] * 2)
        self.assertEqual(mock_browser.call_count, 2)
        mock_updater.assert_called()

    @patch("selex.driver.update_geckodriver")  # must patch in selex.driver namespace because update_geckodriver is imported there
    @patch("selenium.webdriver.Firefox.__init__")
    def test_firefox_driver_mismatch(self, mock_browser, mock_updater):
        mock_browser.side_effect = [SessionNotCreatedException, None]
        Driver(FIREFOX, **KWARGS)
        mock_browser.assert_has_calls([call(ANY, **KWARGS)] * 2)
        self.assertEqual(mock_browser.call_count, 2)
        mock_updater.assert_called()

    @patch("selenium.webdriver.Ie.__init__")
    def test_ie_driver_mismatch(self, mock_browser):
        mock_browser.side_effect = [SessionNotCreatedException, None]
        with self.assertRaises(SessionNotCreatedException):
            Driver(IE, **KWARGS)
        mock_browser.assert_called_once_with(ANY, **KWARGS)

    @patch("selenium.webdriver.Edge.__init__")
    def test_edge_driver_mismatch(self, mock_browser):
        mock_browser.side_effect = [SessionNotCreatedException, None]
        with self.assertRaises(SessionNotCreatedException):
            Driver(EDGE, **KWARGS)
        mock_browser.assert_called_once_with(ANY, **KWARGS)


class ChromeOptionsTest(unittest.TestCase):
    """
    Tests additional options for ChromeDriver initialization.
    """
    
    def test_chrome_options(self):
        args = chrome_options(user_data_path=USER_DATA_PATH, profile_name=USER_PROFILE).arguments
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0], f'--user-data-dir={USER_DATA_PATH}')
        self.assertEqual(args[1], f'--profile-directory={USER_PROFILE}')
        self.assertEqual(args[2], '--disable-blink-features=AutomationControlled')
        
    def test_chrome_options_default(self):
        args = chrome_options(user_data_path=USER_DATA_PATH).arguments
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0], f'--user-data-dir={USER_DATA_PATH}')
        self.assertEqual(args[1], f'--profile-directory=Default')
        self.assertEqual(args[2], '--disable-blink-features=AutomationControlled')


if __name__ == "__main__":
    unittest.main(exit=False)
