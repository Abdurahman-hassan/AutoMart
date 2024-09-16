from django.conf import settings
import os

try:
    OCTO_LOGGER_NAME = settings.OCTO_LOGGER_NAME
except AttributeError:
    OCTO_LOGGER_NAME = "octo-log"


def get_logging(name: str | None = OCTO_LOGGER_NAME):
    return name, {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s[%(asctime)s] [%(process)d] [%(module)s] [%(levelname)s] %(message)s %(reset)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
                "style": "%",
            },
        },
        "handlers": {
            f"{name}": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": os.path.join(settings.BASE_DIR, f"logs/{name}.log"),
                "formatter": "colored",
            },
        },
        "loggers": {
            f"{name}": {
                "handlers": [f"{name}"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
