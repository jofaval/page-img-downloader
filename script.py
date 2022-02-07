# For requests
from typing import List
import requests
# For parsing the HTML
from bs4 import BeautifulSoup
# For system operations, clean console and create directories
import os
# To validate the URL of the requests
import validators
# To save files in binary (images)
import shutil
# To be able to generate a queue of concurrent threads (simultaneous)
from concurrent.futures import ThreadPoolExecutor
# To safely close the context of a variable
from contextlib import closing

# Typing imports
from requests.models import Response

CONF = {
    'IMAGES_DIR': os.path.join(os.getcwd(), 'images'),
    'REQUEST_SESSION': requests.Session(),
    'DEBUG': False,
    'HEADERS': { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36' },
    'TIMEOUT': (3.05, 27),
    'PARSER': 'lxml',
    'THREADS_LIMIT': 25,
}

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
    if CONF['DEBUG']: print('Se va a recuperar el contenido de la página', url)

    if not (validators.url(url)):
        if CONF['DEBUG']: print('La URL no es válida, no se ha podido descargar el contenido')
        return ''

    with closing( CONF['REQUEST_SESSION'].get(url, timeout=CONF['TIMEOUT'], headers=CONF['HEADERS'], stream=True) ) as res:
        # The answer has failed
        if not is_success(res):
            if CONF['DEBUG']: print('No se ha podido recuperar el contenido de la página correctamente')
            return ''

        # If the .text is returned and not the .content, the return of binary values ​​is avoided
        html = res.text
        if display: print(res.status_code, html)

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

    get_src = lambda image: image['src']
    is_valid_image = lambda image: True

    images_links = [ get_src(image) for image in images if is_valid_image(image) ]

    print(images_links)

    return list( set(images_links) )


def create_folder_if_not_exists(folder: str) -> None:
    """
    Creates a folder if doesn't previously exist

    folder : str
        The folder name

    returns None
    """
    if not os.path.exists(folder): os.makedirs(folder)

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

    img_content = requests.get(url, stream = True)
    img_content.raw.decode_content = True

    with open(os.path.join(CONF['IMAGES_DIR'], filename), "wb") as img_file:
        shutil.copyfileobj(img_content.raw, img_file)

def download_imgs(website_url: str) -> None:
    """
    Downloads imgs from a website

    website_url : str
        The website's URL

    returns None
    """
    create_folder_if_not_exists(CONF['IMAGES_DIR'])

    images_links = get_imgs_links_from_website(website_url)

    start_url = ''

    # Prepare the images data
    images = []
    index = 0
    for url in images_links:
        index += 1
        if start_url: url = f'{start_url}{url}'
        images.append((url, f'{index}.jpg',))
    
    print(images)

    # Actually download the images
    with ThreadPoolExecutor(CONF['THREADS_LIMIT']) as executor:
        executor.map(download_img, images)
        executor.shutdown()

def main() -> None:
    """
    Main flow of execution of the website
    
    returns None
    """
    download_imgs('')

if __name__ == '__main__':
    main()