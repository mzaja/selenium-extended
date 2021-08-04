import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import selex.updater.firefox    # must import like this before "from A import B", else function B is not patchable
from selex.updater.firefox import (get_firefox_bit_version_win, 
                                   get_geckodriver_version_win, 
                                   get_latest_geckodriver_version,
                                   locate_geckodriver,
                                   update_geckodriver)


@patch.object(Path, "exists")
class GetFirefoxBitVersionTest(unittest.TestCase):
    """
    Tests the 'get_firefox_bit_version_win' function.
    
    This is not a proper unit test beause it relies on knowing the
    internal workings of the function, not a set of defined inputs
    and outputs.
    """
    def test_64(self, mock_exists):
        mock_exists.side_effect = [True, False]     # return values in this order
        self.assertEqual(get_firefox_bit_version_win(), 64)
    
    def test_32(self, mock_exists):
        mock_exists.side_effect = [False, True]
        self.assertEqual(get_firefox_bit_version_win(), 32)

    def test_both(self, mock_exists):
        mock_exists.side_effect = [True, True]
        self.assertEqual(get_firefox_bit_version_win(), 64)

    def test_none(self, mock_exists):
        mock_exists.side_effect = [False, False]
        self.assertEqual(get_firefox_bit_version_win(), None)


@patch("selex.updater.firefox.locate_generic_driver")
class LocateGeckoDriverTest(unittest.TestCase):
    """
    Tests the 'locate_geckodriver' function.
    """
    def test_forwarding_return_value(self, mock_locate_generic_driver):
        return_values = ["A", "B", "C", None]
        mock_locate_generic_driver.side_effect = return_values 
        for retval in return_values:
            self.assertEqual(locate_geckodriver(), retval)


@patch("subprocess.check_output")
@patch("selex.updater.firefox.locate_geckodriver")
class GetGeckoDriverVersionTest(unittest.TestCase):
    """
    Tests the 'get_geckodriver_version_win' function.
    """
    VERSION = "0.29.1"
    SHELL_RAW_OUTPUT = b"""geckodriver 0.29.1 (970ef713fe58 2021-04-08 23:34 +0200)\n\n
The source code of this program is available from\ntesting/geckodriver
in https://hg.mozilla.org/mozilla-central.\n\nThis program is subject 
to the terms of the Mozilla Public License 2.0.\nYou can obtain a copy 
of the license at https://mozilla.org/MPL/2.0/.\n"""
    
    def test_path_provided(self, mock_locate_geckodriver, mock_check_output):
        mock_check_output.return_value = self.SHELL_RAW_OUTPUT
        self.assertEqual(self.VERSION, get_geckodriver_version_win("2012/metalfest/"))
        mock_locate_geckodriver.assert_not_called()
    
    def test_path_not_provided(self, mock_locate_geckodriver, mock_check_output):
        mock_check_output.return_value = self.SHELL_RAW_OUTPUT
        self.assertEqual(self.VERSION, get_geckodriver_version_win())
        mock_locate_geckodriver.assert_called_once()


if __name__ == "__main__":
    unittest.main(exit=False)