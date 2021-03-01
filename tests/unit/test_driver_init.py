import unittest

from selex import Driver, chrome_options

USER_DATA_PATH = "dummy/user/data/path"
USER_PROFILE = "Profile 99"

class DriverInit(unittest.TestCase):
    """Test the initialization of the Driver class"""
    
    def test_wrong_browser_choice(self):
        with self.assertRaises(ValueError):
            driver = Driver("No such browser!")
    
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


if __name__ == "__main__":
    unittest.main(exit=False)