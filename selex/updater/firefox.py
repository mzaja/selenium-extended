import re
import requests
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup

from selex.const import CMD_OUT_DECODING
from .generic import locate_generic_driver, newer_version_available, zip_download_and_extract


GECKODRIVER = "GeckoDriver"
GECKODRIVER_EXE = "geckodriver.exe"
GECKODRIVER_DOWNLOADS_URL = "https://github.com/mozilla/geckodriver/releases/latest"

geckodriver_version_regex = re.compile(r"geckodriver ([0-9\.]+)")


def get_firefox_bit_version_win():
    """
    Returns the installed Firefox version (64 or 32 bit) on Windows. 
    If both version are installed, 64 is returned.
    """
    for version, suffix in zip([64, 32], ['', ' (x86)']):
        if Path(fr"C:\Program Files{suffix}\Mozilla Firefox").exists():
            return version
    

def locate_geckodriver() -> Path:
    """
    Locates the first available geckodriver.exe on system path.
    """
    return locate_generic_driver(GECKODRIVER_EXE)


def get_geckodriver_version_win(geckodriver_path: str = None) -> str:
    """
    Returns the current geckodriver.exe version as string.
    """
    if geckodriver_path == None:
        geckodriver_path = locate_geckodriver()
    shell_out = subprocess.check_output(f"{geckodriver_path} --version", shell=True).decode(CMD_OUT_DECODING).strip()
    return geckodriver_version_regex.search(shell_out).group(1)


def get_latest_geckodriver_version():
    """
    Returns the latest available geckodriver release version from GitHub.
    """
    href_regex = re.compile("/mozilla/geckodriver/releases/tag/")
    link_text = BeautifulSoup(requests.get(GECKODRIVER_DOWNLOADS_URL).text, features="html.parser").find("a", href=href_regex).text
    return link_text.strip().replace('v','')    # remove whitespace and preceeding 'v' character


def update_geckodriver(force: bool = False):
    """
    Updates ChromeDriver to match the current Chrome version.
    
    Parameters:
        force (bool): If True, ChromeDriver will be updated even if the major version number
                      matches the one from Chrome. If False, ChromeDriver is updated only on
                      the major version number mismatch.
    """
    geckodriver_path = locate_geckodriver()
    current_version = get_geckodriver_version_win(geckodriver_path)
    latest_version = get_latest_geckodriver_version()
    
    print(f"Current {GECKODRIVER} version is {current_version}.")
    print(f"Latest {GECKODRIVER} version is {latest_version}.")
    
    if (newer_version_available(current_version, latest_version) or (True == force)):
        print(f"Updating {GECKODRIVER}...")
        firefox_bits = get_firefox_bit_version_win()
        download_link = f"https://github.com/mozilla/geckodriver/releases/download/v{latest_version}/geckodriver-v{latest_version}-win{firefox_bits}.zip"
        zip_download_and_extract(download_link, geckodriver_path.parent, [GECKODRIVER_EXE])
        print(f"{GECKODRIVER} updated to {latest_version}.")
    else:
        print("No update needed.")
        