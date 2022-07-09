from os import getcwd
from os.path import join
from requests import Session
from multiprocessing import cpu_count
import logging

# total number of multiprocessors available
PROCESSORS = cpu_count() - 1

CONF = {
    'IMAGES_DIR': join(getcwd(), 'images'),
    'REQUEST_SESSION': Session(),
    'DEBUG': True,
    'HEADERS': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'},
    'TIMEOUT': (3.05, 27),
    'PARSER': 'lxml',
    'THREADS_LIMIT': PROCESSORS,
    'DEFAULT_LOCALE': 'es',
    'LOGGING': {
        'NAME': 'page-img-downloader',
        # 'FORMAT': '%(asctime)s %(clientip)-15s %(user)-8s %(message)s',
        'FORMAT': '[%(asctime)s] %(levelname)s - %(message)s',
        'LEVEL': logging.DEBUG,
        'FILENAME': 'log.txt',
        'FILE_MODE': 'a+',
    },
    'STRINGS': {
        'es': {
            'STARTING': 'Se va a recuperar el contenido de la página',
            'INVALID_URL': 'La URL no es válida, no se ha podido descargar el contenido',
            'CONTENT_NOT_RETRIEVED': 'No se ha podido recuperar el contenido de la página correctamente',
            'DOWNLOAD_FAILURE': 'Algo ha fallado al intentar descargar:',
            'INPUT_WEBSITE': '¿Sobre qué página te gustaría trabajar?',
        },
        'en': {
            'STARTING': "The page's content is going to be retrieved",
            'INVALID_URL': 'Invalid url, the content could not be downloaded',
            'CONTENT_NOT_RETRIEVED': "Could not successfully retrieve the page's content",
            'DOWNLOAD_FAILURE': 'Something went wrong while trying to download',
            'INPUT_WEBSITE': 'What website would you want to download from?',
        }
    },
}
