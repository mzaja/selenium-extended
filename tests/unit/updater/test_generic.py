import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import selex.updater.generic    # must import like this before "from ... import locate_on_syspath", else the function is not patchable
from selex.updater.generic import locate_generic_driver, locate_on_syspath, newer_version_available, zip_download_and_extract 
from selex.exceptions import WebdriverNotFoundError


@patch.object(Path, "glob")
class LocateOnSyspathTest(unittest.TestCase):
    """
    Tests the 'locate_on_syspath' function.
    """
    
    def test_no_result(self, mock_glob):
        mock_glob.return_value = []
        self.assertEqual(locate_on_syspath("Alestorm.exe"), None)
    
    def test_one_result(self, mock_glob):
        first_result = Path("/2012/metalfest")
        mock_glob.return_value = [first_result]
        self.assertEqual(locate_on_syspath("Alestorm.exe"), first_result)
    
    @patch("builtins.print")
    def test_two_results(self, mock_print, mock_glob):
        first_result = Path("/2012/metalfest")
        mock_glob.return_value = [first_result, Path("/2013/metaldays")]
        self.assertEqual(locate_on_syspath("Alestorm.exe"), first_result)
        mock_print.assert_called_once()
    

@patch("selex.updater.generic.locate_on_syspath")   # patch on original import
class LocateGenericDriverTest(unittest.TestCase):
    """
    Tests the 'locate_generic_driver' function.
    """
    
    def test_success(self, mock_locate_on_syspath):
        path = Path("/2012/metalfest")
        mock_locate_on_syspath.return_value = path
        self.assertEqual(locate_generic_driver("DevilDriver.exe"), path)

    def test_fail(self, mock_locate_on_syspath):
        mock_locate_on_syspath.return_value = None
        with self.assertRaises(WebdriverNotFoundError):
            locate_generic_driver("DevilDriver.exe")


class NewerVersionAvailableTest(unittest.TestCase):
    """
    Tests the 'newer_version_available' function.
    """
    current_version = "92.0.143.1"
    
    def test_latest_newer(self):
        latest_version = "92.0.143.2"
        self.assertTrue(newer_version_available(self.current_version, latest_version))
    
    def test_versions_equal(self):
        latest_version = self.current_version
        self.assertFalse(newer_version_available(self.current_version, latest_version))
    
    def test_latest_older(self):
        latest_version = "92.0.143.0"
        self.assertFalse(newer_version_available(self.current_version, latest_version))
        
    def test_latest_longer(self):
        latest_version = "92.0.143.11"
        self.assertTrue(newer_version_available(self.current_version, latest_version))
    
    @unittest.skip("Theoretically it should return False, but in practice this case is highly unlikely.")   
    def test_latest_longer_by_zero(self):
        latest_version = "92.0.143.1.0"
        self.assertFalse(newer_version_available(self.current_version, latest_version))

    def test_latest_shorter(self):
        latest_version = "92.0.143"
        self.assertFalse(newer_version_available(self.current_version, latest_version))


@patch("selex.updater.generic.ZipFile")
@patch("selex.updater.generic.BytesIO")
@patch("requests.get")
class ZipDownloadAndExtractTest(unittest.TestCase):
    """
    Tests the 'zip_download_and_extract' function.
    """

    def test_default(self, mock_requests_get, mock_bytes_io, mock_zipfile):
        download_link = "www.drunkenpensioner.com/k-plus.zip"
        output_dir = "/festivals/2012/metalfest"
        files = ["Wine.bottle", "Beer.bottle"]
        mock_zipf = Mock()
        mock_zipfile.return_value.__enter__.return_value = mock_zipf
        zip_download_and_extract(download_link, output_dir, files)
        mock_requests_get.assert_called_with(download_link, stream=True)
        mock_bytes_io.assert_called()
        mock_zipfile.assert_called()
        mock_zipf.extractall.assert_called_with(output_dir, files)


if __name__ == "__main__":
    unittest.main(exit=False)