import re
import requests
import subprocess
from collections import namedtuple
from pathlib import Path

from bs4 import BeautifulSoup

from selex.const import CMD_OUT_DECODING, CHROME
from selex.exceptions import BrowserVersionUndeterminedError, NoSuchChromeDriverError
from .generic import locate_generic_driver, newer_version_available, zip_download_and_extract


CHROME_PATH_WIN_32 = r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
CHROME_PATH_WIN_64 = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CHROMEDRIVER_INDEX_URL = "https://chromedriver.storage.googleapis.com/index.html"  # unused 
CHROMEDRIVER_LATEST_RELEASE = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
CHROMEDRIVER_DOWNLOADS_URL = "https://chromedriver.chromium.org/downloads"
CHROMEDRIVER_API_HOME_URL = "https://chromedriver.storage.googleapis.com"
CHROMEDRIVER_ZIP_WIN32 = "chromedriver_win32.zip"
CHROMEDRIVER_EXE = "chromedriver.exe"
CHROMEDRIVER = "ChromeDriver"

chrome_version_regex = re.compile(r"Version=([\d\.]+)")
chromedriver_version_regex = re.compile(fr"{CHROMEDRIVER} ([\d\.]+)")

ChromeVersion = namedtuple("ChromeVersion", ["major", "minor", "build", "sub"], defaults = 4*["0"])


def get_chrome_version_win(chrome_exe_path: str = None) -> str:
    """
    Retrieves the Chrome version on the Windows platform. 
    Checks the default installation folders of 32 and 64 bit versions.
    A custom Chrome exe path can also be specified.
    """
    chrome_paths = [CHROME_PATH_WIN_64, CHROME_PATH_WIN_32]
    if chrome_exe_path is not None: 
        chrome_paths.insert(0, chrome_exe_path) # prepend custom path to start
    for path in chrome_paths:
        query = "wmic datafile where name=\"" + path + "\" get Version /value"   # problematic with f-strings
        shell_out = subprocess.check_output(query, shell=True).decode(CMD_OUT_DECODING).strip()
        if shell_out != "": 
            break
    try:
        return chrome_version_regex.search(shell_out).group(1)
    except AttributeError:
        raise BrowserVersionUndeterminedError(CHROME, chrome_paths)


def locate_chromedriver()-> Path:
    """
    Locates the first available chromedriver.exe on system path.
    """
    return locate_generic_driver(CHROMEDRIVER_EXE)


def get_chromedriver_version_win(chromedriver_path: str = None) -> int:
    """
    Retrieves the ChromeDriver version on the Windows platform.
    """
    if chromedriver_path is None:
        chromedriver_path = locate_chromedriver()
    shell_out = subprocess.check_output(f"{chromedriver_path} -v", shell=True).decode(CMD_OUT_DECODING).strip()
    return chromedriver_version_regex.search(shell_out).group(1)


def get_latest_chromedriver_version(major_version: int = None, include_beta: False = False):
    """
    Returns the latest ChromeDriver version available for download.
    
    Parameters:
        major_version (int): Searches for the latest ChromeDriver for this particular major release version. 
                             If None is provided, searches for the latest stable major release.
        include_beta (bool): If True, search results include the ChromeDriver for the current Chrome beta release (if one exists).
                             'major_version' parameter is disregarded in this case.
    """
    if True == include_beta:    # if beta versions are included, search the downloads page
        return chromedriver_version_regex.search(\
            BeautifulSoup(requests.get(CHROMEDRIVER_DOWNLOADS_URL).text, features="html.parser")\
                .find("a", text=chromedriver_version_regex).text).group(1)
    else:   # otherwise access the LATEST_RELEASE file to get the latest version (much quicker)
        if None == major_version:
            return requests.get(CHROMEDRIVER_LATEST_RELEASE).text
        else:
            version = requests.get(f"{CHROMEDRIVER_LATEST_RELEASE}_{major_version}").text
            if not version.startswith(str(major_version)):  # if the received response is invalid
                raise NoSuchChromeDriverError(major_version)
            else:
                return version


def parse_chrome_version(version_string: str):
    """
    Returns a named tuple containing the major, minor, build and sub version of Chrome or ChromeDriver.
    """
    return (ChromeVersion(*version_string.split('.')))


def update_chromedriver(force: bool = False):
    """
    Updates ChromeDriver matching the Chrome's major release version. 
    If the major versions already match, it looks for ChromeDriver updates for that particular major release.
    
    Parameters:
        force (bool): If True, ChromeDriver will be updated even if the major version number
                      matches the one from Chrome. If False, ChromeDriver is updated only on
                      the major version number mismatch.
    """
    browser_version_full = get_chrome_version_win()
    browser_version_major = parse_chrome_version(browser_version_full).major
    
    driver_path = locate_chromedriver()
    driver_version = get_chromedriver_version_win(driver_path)
    latest_driver_version = get_latest_chromedriver_version(browser_version_major)  # only consider drivers suitable for the current browser
    
    print(f"{CHROME} version is {browser_version_full}.")
    print(f"{CHROMEDRIVER} version is {driver_version}.")
    print(f"{CHROMEDRIVER} version {latest_driver_version} is available.")
    
    if  (newer_version_available(driver_version, latest_driver_version) or
        (browser_version_major != parse_chrome_version(latest_driver_version).major) or  # if a downgrade is required (old browser)
        (True == force)):
        print(f"Updating {CHROMEDRIVER}...")
        download_link = f"{CHROMEDRIVER_API_HOME_URL}/{latest_driver_version}/{CHROMEDRIVER_ZIP_WIN32}"
        zip_download_and_extract(download_link, driver_path.parent, [CHROMEDRIVER_EXE])
        print(f"{CHROMEDRIVER} updated to {latest_driver_version}.")
    else:
        print("No update needed.")
        