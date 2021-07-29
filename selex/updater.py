import pathlib
import re
import requests
import subprocess
import sys
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile

from selex.exceptions import ChromedriverNotFoundError, ChromeVersionUndeterminedError


CHROME_PATH_WIN = r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
CMD_OUT_DECODING = "utf-8"

CHROMEDRIVER_INDEX_URL = "https://chromedriver.storage.googleapis.com/index.html"  # unused 
CHROMEDRIVER_DOWNLOADS_PAGE = "https://chromedriver.chromium.org/downloads"
CHROMEDRIVER_API_HOME = "https://chromedriver.storage.googleapis.com"
CHROMEDRIVER_ZIP_WIN32 = "chromedriver_win32.zip"
CHROMEDRIVER_EXE = "chromedriver.exe"
ChromeDriver = "ChromeDriver"

chrome_version_regex = re.compile(r"Version=(\d+)\.")
chromedriver_version_regex = re.compile(fr"{ChromeDriver} (\d+)\.")


def get_chrome_version_win(chrome_exe_path: str = None):
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
        raise ChromeVersionUndeterminedError(chrome_exe_path)


def locate_chromedriver():
    """
    Locates the first available chromedriver in PATH.
    """
    for path in sys.path:
        search_results = list(pathlib.Path(path).glob(CHROMEDRIVER_EXE))
        if len(search_results) > 0:  # if file found
            return search_results[0]
    raise ChromedriverNotFoundError # if the search yielded no results


def get_chromedriver_version_win(chromedriver_path: str = None):
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
    print(f"{ChromeDriver} version is {chromedriver_version}.")
    print(f"Updating {ChromeDriver}...")
    if ((chrome_version != chromedriver_version) or (True == force)):
        hyperlink_text = BeautifulSoup(requests.get(CHROMEDRIVER_DOWNLOADS_PAGE).text, features="html.parser").find("a", text=re.compile(f"{ChromeDriver} {chrome_version}")).text
        new_chromedriver_version = re.search(f"{ChromeDriver} (.*)", hyperlink_text).group(1)
        download_link = f"{CHROMEDRIVER_API_HOME}/{new_chromedriver_version}/{CHROMEDRIVER_ZIP_WIN32}"
        with ZipFile(BytesIO(requests.get(download_link, stream=True).content)) as zipf:
            zipf.extract(CHROMEDRIVER_EXE, chromedriver_path.parent)
        print(f"{ChromeDriver} updated to {new_chromedriver_version}.")
    else:
        print("No update needed.")