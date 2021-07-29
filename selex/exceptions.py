class SelexException(Exception):
    pass

class ChromeVersionUndeterminedError(SelexException):
    """doc"""
    def __init__(self, chrome_exe_path: str):
        super().__init__(f"Chrome version cannot be determined. Is 'chrome.exe' located at '{chrome_exe_path}'?")
        

class ChromedriverNotFoundError(SelexException):
    """doc"""
    def __init__(self):
        super().__init__("'chromedriver.exe' cannot be found on Python path!")
