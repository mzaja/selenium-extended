import unittest
from pathlib import Path
from unittest.mock import patch

import selex.updater.chrome    # must import like this before "from A import B", else function B is not patchable
from selex.updater.chrome import (get_chrome_version_win, 
                                  get_chromedriver_version_win,
                                  get_latest_chromedriver_version,
                                  locate_chromedriver,
                                  parse_chrome_version,
                                  update_chromedriver,
                                  CHROME_PATH_WIN)

from selex.exceptions import BrowserVersionUndeterminedError, NoSuchChromeDriverError


@patch("subprocess.check_output")
class GetChromeVersionTest(unittest.TestCase):
    """
    Tests the 'get_chrome_version_win' function.
    """
    VERSION = "92.0.4515.131"
    SHELL_RAW_OUTPUT = b'\r\r\n\r\r\nVersion=92.0.4515.131\r\r\n\r\r\n\r\r\n\r\r\n'
    
    def test_path_provided(self, mock_check_output):
        chrome_path = "2012/metalfest/chrome.exe"
        mock_check_output.return_value = self.SHELL_RAW_OUTPUT
        self.assertEqual(get_chrome_version_win("2012/metalfest/chrome.exe"), self.VERSION)
        self.assertIn(chrome_path, mock_check_output.call_args[0][0])  # assert path in query

    def test_path_not_provided(self, mock_check_output):
        mock_check_output.return_value = self.SHELL_RAW_OUTPUT
        self.assertEqual(get_chrome_version_win(), self.VERSION)
        self.assertIn(CHROME_PATH_WIN, mock_check_output.call_args[0][0])  # assert path in query
    
    def test_invalid_response(self, mock_check_output): 
        """Normally this raises a subprocess error, but we can also raise one."""
        mock_check_output.return_value = b"Some nonsense"
        with self.assertRaises(BrowserVersionUndeterminedError):
            get_chrome_version_win()


@patch("selex.updater.chrome.locate_generic_driver")
class LocateChromeDriverTest(unittest.TestCase):
    """
    Tests the 'locate_chromedriver' function.
    """
    def test_forwarding_return_value(self, mock_locate_generic_driver):
        return_values = [Path(x) for x in ["A", "B", "C"]]
        mock_locate_generic_driver.side_effect = return_values 
        for retval in return_values:
            self.assertEqual(locate_chromedriver(), retval)


@patch("subprocess.check_output")
@patch("selex.updater.chrome.locate_chromedriver")
class GetChromeDriverVersionTest(unittest.TestCase):
    """
    Tests the 'get_chromedriver_version_win' function.
    """
    VERSION = "92.0.4515.107"
    SHELL_RAW_OUTPUT = b'ChromeDriver 92.0.4515.107 (87a818b10553a07434ea9e2b6dccf3cbe7895134-refs/branch-heads/4515@{#1634})\r\n'
    
    def test_path_provided(self, mock_locate_chromedriver, mock_check_output):
        mock_check_output.return_value = self.SHELL_RAW_OUTPUT
        self.assertEqual(self.VERSION, get_chromedriver_version_win("2012/metalfest/chromedriver.exe"))
        mock_locate_chromedriver.assert_not_called()
    
    def test_path_not_provided(self, mock_locate_chromedriver, mock_check_output):
        mock_check_output.return_value = self.SHELL_RAW_OUTPUT
        self.assertEqual(self.VERSION, get_chromedriver_version_win())
        mock_locate_chromedriver.assert_called_once()


@patch("requests.get")
class GetLatestChromeDriverVersionTest(unittest.TestCase):
    """
    Tests the 'get_latest_chromedriver_version' function.
    
    Uses a real website snapshot.
    """
    VERSION_BETA = "93.0.4577.15"
    VERSION_92 = "92.0.4515.107"
    VERSION_87 = "87.0.4280.88"
    INVALID_VERSION_RESPONSE = """<?xml version='1.0' encoding='UTF-8'?><Error><Code>NoSuchKey</Code>
<Message>The specified key does not exist.</Message><Details>No such object: chromedriver/LATEST_RELEASE_999</Details></Error>"""
    
    def test_beta_version(self, mock_requests_get):
        VERSION = self.VERSION_BETA
        mock_website_path = Path("tests/resources/chromedriver_downloads_page.html")
        for major_version in [None, 87]:     # major version should not matter; need to use a loop because the text stream is exhausted after 1 read
            with open(mock_website_path, "r",encoding="utf-8") as mock_website: 
                mock_requests_get.return_value.text = mock_website
                self.assertEqual(VERSION, get_latest_chromedriver_version(include_beta=True, major_version=major_version)) 

    def test_latest_stable_version(self, mock_requests_get):
        VERSION = self.VERSION_92
        mock_requests_get.return_value.text = VERSION  # returns the version directly, but that could change in the future
        self.assertEqual(VERSION, get_latest_chromedriver_version())
    
    def test_specific_major_version(self, mock_requests_get):
        VERSION = self.VERSION_87
        mock_requests_get.return_value.text = VERSION  # returns the version directly, but that could change in the future
        self.assertEqual(VERSION, get_latest_chromedriver_version(major_version=87))

    def test_invalid_major_version(self, mock_requests_get):
        INVALID_VERSION = 999
        mock_requests_get.return_value.text = self.INVALID_VERSION_RESPONSE  # response received when an invalid version is requested
        with self.assertRaisesRegex(NoSuchChromeDriverError, str(INVALID_VERSION)):
            get_latest_chromedriver_version(major_version=INVALID_VERSION)
            

class ParseChromeDriverTest(unittest.TestCase):
    """
    Tests the 'parse_chrome_version' function.
    """
    def test_parsing_complete(self):
        result = parse_chrome_version("92.0.4515.107")
        self.assertEqual(result.major, "92")
        self.assertEqual(result.minor, "0")
        self.assertEqual(result.build, "4515")
        self.assertEqual(result.sub, "107")

    def test_parsing_incomplete(self):
        result = parse_chrome_version("92")
        self.assertEqual(result.major, "92")
        self.assertEqual(result.minor, "0")
        self.assertEqual(result.build, "0")
        self.assertEqual(result.sub, "0")
        

class UpdateChromeDriverTest(unittest.TestCase):
    """
    Tests the 'update_chromedriver' function.
    """
    CURRENT_DRIVER_VERSION = "92.0.4515.107"
    CURRENT_BROWSER_VERSION = "92.0.4515.131"
    CHROMEDRIVER_PATH = Path("2013/metaldays/chromedriver.exe")
    
    @patch("builtins.print")
    @patch("selex.updater.chrome.zip_download_and_extract")
    @patch("selex.updater.chrome.get_chrome_version_win")
    @patch("selex.updater.chrome.get_latest_chromedriver_version")
    @patch("selex.updater.chrome.get_chromedriver_version_win")
    @patch("selex.updater.chrome.locate_chromedriver")
    def base_test(self, 
                    mock_locate_chromedriver, 
                    mock_get_chromedriver_version_win,
                    mock_get_latest_chromedriver_version,
                    mock_get_chrome_version_win,
                    mock_zip_download_and_extract,
                    mock_print,
                    force_update: bool,
                    latest_driver_version: str,
                    update_triggered: bool):
        
        mock_locate_chromedriver.return_value = self.CHROMEDRIVER_PATH
        mock_get_chrome_version_win.return_value = self.CURRENT_BROWSER_VERSION
        mock_get_chromedriver_version_win.return_value = self.CURRENT_DRIVER_VERSION
        mock_get_latest_chromedriver_version.return_value = latest_driver_version 
        
        update_chromedriver(force = force_update)
        
        mock_locate_chromedriver.assert_called_once()
        mock_get_chromedriver_version_win.assert_called_once_with(self.CHROMEDRIVER_PATH)
        mock_get_latest_chromedriver_version.assert_called_once()
        mock_get_chrome_version_win.assert_called_once()
        
        if True == update_triggered:
            mock_zip_download_and_extract.assert_called_once()
            self.assertEqual(mock_print.call_count, 5)
        else:
            mock_zip_download_and_extract.assert_not_called()
            self.assertEqual(mock_print.call_count, 4)
        
        
    def base_test_runner(self, force_update:bool, latest_driver_version: str, update_triggered: bool):
        """Wraps the base test so that keyword arguments are shown in test cases' signature."""
        self.base_test(force_update = force_update, 
                       latest_driver_version = latest_driver_version, 
                       update_triggered = update_triggered)

    
    def test_newer_exists(self):
        """Tests the case when a newer version exists."""
        self.base_test_runner(force_update = False, 
                              latest_driver_version = "92.0.4515.234",
                              update_triggered = True)
    

    def test_newer_does_not_exist_force(self):
        """Tests the case when a newer version does not exist."""
        self.base_test_runner(force_update = False, 
                              latest_driver_version = self.CURRENT_DRIVER_VERSION,
                              update_triggered = False)
    
    
    def test_newer_does_not_exist_force(self):
        """Tests the case when a newer version does not exist but an update is forced nevertheless."""
        self.base_test_runner(force_update = True, 
                              latest_driver_version = self.CURRENT_DRIVER_VERSION,
                              update_triggered = True)
        
    def test_downgrade(self):
        """Tests the case when the major browser version is older than the current driver version."""
        self.base_test_runner(force_update = False, 
                        latest_driver_version = "93.0.4577.15",
                        update_triggered = True)

 
if __name__ == "__main__":
    unittest.main(exit=False)