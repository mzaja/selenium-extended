import re
import requests
import subprocess
from bs4 import BeautifulSoup

from selex.const import CMD_OUT_DECODING, CHROME
from selex.exceptions import BrowserVersionUndeterminedError
from .generic import locate_generic_driver, zip_download_and_extract


CHROME_PATH_WIN = r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
CHROMEDRIVER_INDEX_URL = "https://chromedriver.storage.googleapis.com/index.html"  # unused 
CHROMEDRIVER_DOWNLOADS_URL = "https://chromedriver.chromium.org/downloads"
CHROMEDRIVER_API_HOME_URL = "https://chromedriver.storage.googleapis.com"
CHROMEDRIVER_ZIP_WIN32 = "chromedriver_win32.zip"
CHROMEDRIVER_EXE = "chromedriver.exe"
CHROMEDRIVER = "ChromeDriver"

chrome_version_regex = re.compile(r"Version=(\d+)\.")
chromedriver_version_regex = re.compile(fr"{CHROMEDRIVER} (\d+)\.")


def get_chrome_version_win(chrome_exe_path: str = None) -> int:
    """
    Retrieves the major Chrome version on the Windows platform. 
    """
    if chrome_exe_path == None: 
        chrome_exe_path = CHROME_PATH_WIN
    query = "wmic datafile where name=\"" + chrome_exe_path + "\" get Version /value"   # problematic with f-strings
    shell_out = subprocess.check_output(query, shell=True).decode(CMD_OUT_DECODING).strip()
    try:
        return int(chrome_version_regex.search(shell_out).group(1))
    except AttributeError:
        raise BrowserVersionUndeterminedError(CHROME, chrome_exe_path)


def locate_chromedriver():
    """
    Locates the first available chromedriver.exe on system path.
    """
    return locate_generic_driver(CHROMEDRIVER_EXE)


def get_chromedriver_version_win(chromedriver_path: str = None) -> int:
    """
    Retrieves the major ChromeDriver version on the Windows platform.
    """
    if chromedriver_path == None:
        chromedriver_path = locate_chromedriver()
    shell_out = subprocess.check_output(f"{chromedriver_path} -v", shell=True).decode(CMD_OUT_DECODING).strip()
    return int(chromedriver_version_regex.search(shell_out).group(1))


def update_chromedriver(force: bool = False):
    """
    Updates ChromeDriver to match the current Chrome version.
    
    Parameters:
        force (bool): If True, ChromeDriver will be updated even if the major version number
                      matches the one from Chrome. If False, ChromeDriver is updated only on
                      the major version number mismatch.
    """
    chrome_version = get_chrome_version_win()
    chromedriver_path = locate_chromedriver()
    chromedriver_version = get_chromedriver_version_win(chromedriver_path)
    print(f"Chrome version is {chrome_version}.")
    print(f"{CHROMEDRIVER} version is {chromedriver_version}.")
    if ((chrome_version != chromedriver_version) or (True == force)):
        print(f"Updating {CHROMEDRIVER}...")
        hyperlink_text = BeautifulSoup(requests.get(CHROMEDRIVER_DOWNLOADS_URL).text, features="html.parser").find("a", text=re.compile(f"{CHROMEDRIVER} {chrome_version}")).text
        new_chromedriver_version = re.search(f"{CHROMEDRIVER} (.*)", hyperlink_text).group(1)
        download_link = f"{CHROMEDRIVER_API_HOME_URL}/{new_chromedriver_version}/{CHROMEDRIVER_ZIP_WIN32}"  # cannot click on hyperlink directly because it uses JavaScript
        zip_download_and_extract(download_link, chromedriver_path.parent, [CHROMEDRIVER_EXE])
        print(f"{CHROMEDRIVER} updated to {new_chromedriver_version}.")
    else:
        print("No update needed.")
        