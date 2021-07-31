class SelexException(Exception):
    pass

class BrowserVersionUndeterminedError(SelexException):
    """Raised when the browser version cannot be determined."""
    def __init__(self, browser_name: str, browser_exe_path: str):
        super().__init__(f"{browser_name} version cannot be determined. Is the browser executable located at '{browser_exe_path}'?")
        
class WebdriverNotFoundError(SelexException):
    """Raised when the webdriver cannot be located on system path."""
    def __init__(self, webdriver_exe: str):
        super().__init__(f"'{webdriver_exe}' cannot be located on system path.")

class NoSuchChromeDriverError(SelexException):
    """Raised when ChromeDriver with the specified major version number cannot be found."""
    def __init__(self, major_version: int):
        super().__init__(f"ChromeDriver {major_version} cannot be found on the downloads website.")