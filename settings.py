import os

CHECK_TIMEOUT = 3
FILE_SONGS_NAMES = os.path.join(os.getcwd(), 'songs.txt') 
SOURCE_LINK = 'http://radiorecord.hostingradio.ru/rr_main96.aacp'
EXECUTE_NAMES = ['Record Dance Radio', 'Radio Record', '- Record News']
CLIENT_LOG_PATH = os.path.join(os.getcwd(), 'log.txt') 
NAME_LOGGER = 'record_logger'
NAME_PARSER = 'Radio Record'
PICTURES_PATH = os.path.join(os.getcwd(), 'pictures') 


def get_pictures():
    di = {}
    for root, dir, files in os.walk(PICTURES_PATH):
        for file in files:
            di[file] = os.path.join(root, file)
    return di

LOG_CONFIG = {
"version": 1,
    "formatters": {
        "standard": {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    "handlers": {
        'console': {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            'stream'  : 'ext://sys.stdout',
        },



        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": f"{CLIENT_LOG_PATH}",
            'maxBytes': 1048576000,
            'backupCount': 3,
        },
    },
    "loggers": {
        "": {
            "handlers": ['console', 'file'], # "file",
            "level": "INFO",
            'propagate': False
        }
    },
}