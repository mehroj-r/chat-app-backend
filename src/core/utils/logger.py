import logging.config
import os

from django.conf import settings

LOG_DIR = settings.LOG_DIR

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        },
        "simple": {
            "format": "%(levelname)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(settings.LOG_DIR, "app.log"),
            "formatter": "detailed",
            "level": "INFO",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(settings.LOG_DIR, "errors.log"),
            "formatter": "detailed",
            "level": "ERROR",
        },
    },
    "root": {
        "handlers": ["console", "file", "error_file"],
        "level": "DEBUG",
    },
}

# Configure the logging system
if not os.path.exists(settings.LOG_DIR):
    os.makedirs(settings.LOG_DIR)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)