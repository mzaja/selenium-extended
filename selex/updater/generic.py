import pathlib
import requests
import sys
from io import BytesIO
from zipfile import ZipFile

from ..exceptions import WebdriverNotFoundError


def locate_on_syspath(pattern: str):
    """
    Locates the first available instance matching the pattern on PATH.
    """
    for path in sys.path:
        search_results = list(pathlib.Path(path).glob(pattern))
        if len(search_results) > 0:  # if file found
            retval = search_results[0]
            if len(search_results) > 1:  # never activated when searching for the exact filename 
                print(f"More than one instance of {pattern} found on PATH. Returning '{retval}'.")
            return retval
    return None


def locate_generic_driver(driver_exe: str):
    """
    Returns the path to the first available instance of the web driver on system path. 
    Raises WebdriverNotFoundError if unsuccessful.
    """
    retval = locate_on_syspath(driver_exe)
    if retval == None:
        raise WebdriverNotFoundError(driver_exe) # if the search yielded no results
    else:
        return retval


def newer_version_available(current_version_local: str, latest_version_online: str):
    """
    Compares two sequences of dot-separated integer strings representing software version numbers. 
    Returns True if the second sequence is greater than the first one.
    """
    return list(map(int, latest_version_online.split('.'))) > list(map(int, current_version_local.split('.')))


def zip_download_and_extract(download_link: str, output_dir: str = None, files: list = None):
    """
    Downloads the Zip file straight to RAM and extracts the nominated files to the output folder.
    
    Parameters:
        download_link (str): URL to the Zip archive.
        output_dir (str): Folder to which the file(s) will be extracted to. Uses CWD if None.
        files (list): Names of files to be extracted. Extracts all if None.
    """
    with ZipFile(BytesIO(requests.get(download_link, stream=True).content)) as zipf:
        zipf.extractall(output_dir, files)
        