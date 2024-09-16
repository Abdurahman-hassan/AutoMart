import logging
import logging.config
from octos.logging.config import get_logging
import re


class Logger:
    def __init__(self, namefile: str | None = None) -> None:
        self._loging_name, self._config = get_logging(name=namefile)

    def get(self) -> logging:
        logging.config.dictConfig(self._config)
        return logging.getLogger(self._loging_name)


def sanitize_message(message: str) -> str:
    """Sanitize the message by removing newlines, tabs,
    and replacing them with spaces."""
    return re.sub(r"[\n\r\t]", " ", message)
