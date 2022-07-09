# For HTTP headers parsing
from cgi import parse_header
# For regex maniupulation
import re
# For url parsing
from urllib.parse import urlparse
# For logging messages in the system
import logging
# For console arguments
from sys import argv
# For requests
from typing import List
import requests
# For parsing the HTML
from bs4 import BeautifulSoup
# For system operations, clean console and create directories
from os import makedirs
from os.path import join, exists, basename
# To validate the URL of the requests
import validators
# To save files in binary (images)
import shutil
# To be able to generate a queue of concurrent threads (simultaneous)
from multiprocessing import Pool
# To safely close the context of a variable
from contextlib import closing
# Typing imports
from requests.models import Response
# The configuration variables
from config import CONF

# The default internalization localization
default_locale = CONF['DEFAULT_LOCALE']
# The logger instance
logger = None


def is_success(res: Response) -> bool:
    """
    Determines wether a request was successful or not

    returns bool
    """
    return not (res.status_code < 200 | res.status_code >= 300)


def get_page(url: str, display: bool = False) -> str:
    """
    Returns the page content if it could be retrieved

    url : str
        The URL from which to retrieve the page's content
    [deprecated] display : bool
        Will it display the content? It will by default

    returns str
    """
    if CONF['DEBUG']:
        logging.info(
            f'{CONF["STRINGS"][default_locale]["INVALID_URL"]} "{url}"')

    if not (validators.url(url)):
        if CONF['DEBUG']:
            logging.error(CONF['STRINGS'][default_locale]['INVALID_URL'])
        return ''

    with closing(CONF['REQUEST_SESSION'].get(url, timeout=CONF['TIMEOUT'], headers=CONF['HEADERS'], stream=True)) as res:
        # The answer has failed
        if not is_success(res):
            if CONF['DEBUG']:
                logging.error(
                    CONF['STRINGS'][default_locale]['CONTENT_NOT_RETRIEVED']
                )
            return ''

        # If the .text is returned and not the .content, the return of binary values ​​is avoided
        html = res.text
        if display:
            print(res.status_code, html)

        return html


def get_imgs_links_from_website(website_url: str) -> List[str]:
    """
    Gets all the img links from a website

    website_url : str
        The website's URL

    returns List[str]
    """
    content = get_page(website_url)

    parsed_content = BeautifulSoup(content, features=CONF['PARSER'])

    images = parsed_content.select('img[src]')

    def get_src(image): return image['src']
    def is_valid_image(image): return True

    images_links = [get_src(image)
                    for image in images if is_valid_image(image)]

    # print(images_links)

    return list(set(images_links))


def create_folder_if_not_exists(folder: str) -> None:
    """
    Creates a folder if doesn't previously exist

    folder : str
        The folder name

    returns None
    """
    if not exists(folder):
        makedirs(folder)


def download_img(data: tuple) -> None:
    """
    Downloads an img

    url : str
        The image's URL
    filename : str
        The file's name

    returns None
    """
    url, filename = data

    try:
        img_content = requests.get(url, stream=True)
        print(dict(img_content.headers).keys())
        img_content.raw.decode_content = True

        # It would be a nice feature, but one that's harder and far more inconsistent
        if 'Content-Disposition' in img_content.headers:
            disposition_headers = img_content.headers['Content-Disposition']
            parsed_disposition_headers = parse_header(disposition_headers)
            http_filename = parsed_disposition_headers['filename']

        with open(join(CONF['IMAGES_DIR'], filename), "wb") as img_file:
            shutil.copyfileobj(img_content.raw, img_file)
    except Exception as error:
        if CONF['DEBUG']:
            logging.error(
                f'{CONF["STRINGS"][default_locale]["DOWNLOAD_FAILURE"]} {url, filename}')
            logging.error(error)


def get_filename(url: str) -> str:
    """
    Get the filename from the URL

    url : str
        The complete URL of the file

    return str
    """
    filename = basename(url)
    # Guard-clause, just in case there's no extension
    if "." not in filename:
        return ''

    if '?' in filename:
        filename = filename[:filename.rindex('?')]

    return filename


def download_imgs(website_url: str) -> None:
    """
    Downloads imgs from a website

    website_url : str
        The website's URL

    returns None
    """
    create_folder_if_not_exists(CONF['IMAGES_DIR'])

    images_links = get_imgs_links_from_website(website_url)
    domain = urlparse(website_url).netloc

    start_url = f'https://{domain}'

    images = []
    # Prepare the images data
    for index, url in enumerate(images_links):
        # secure/guarantee that the url will always start with http protocol
        if start_url and (not url.startswith('http')):
            url = re.sub('\/+', '/', url)
            # it must not start with a separator for the joiner to properly work
            while url.startswith('/'):
                url = url[1:]
            url = join(start_url, url)
            # print('url', start_url, url)

        # extract the filename
        filename = get_filename(url)
        if not filename:
            filename = f'{index + 1}.jpg'

        images.append((url, filename))

    # print(images)

    # Actually download the images
    with Pool(CONF['THREADS_LIMIT']) as executor:
        executor.map(download_img, images)


def get_website() -> str:
    """
    Interact with the user to retrieve the desired website

    returns str
    """
    website = ''
    if len(argv) > 1:
        website = argv[-1]
    else:
        website = input(CONF['STRINGS'][default_locale]['INPUT_WEBSITE'])
    return website


def configure_logger() -> None:
    """
    Configures the logger for this application

    returns None
    """
    global logger
    logging.basicConfig(
        format=CONF['LOGGING']['FORMAT'],
        filename=CONF['LOGGING']['FILENAME'],
        level=CONF['LOGGING']['LEVEL'],
        filemode=CONF['LOGGING']['FILE_MODE'],
    )
    logger = logging.getLogger(CONF['LOGGING']['NAME'])


def main() -> None:
    """
    Main flow of execution of the website

    returns None
    """
    configure_logger()
    website = get_website()
    download_imgs(website)


if __name__ == '__main__':
    main()
