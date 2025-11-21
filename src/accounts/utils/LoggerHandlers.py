from logging import StreamHandler, Formatter
from logging.handlers import TimedRotatingFileHandler

from ..core.config import settings
from .LoggerColorFormatter import ColorFormatter

def get_console_handler():
    console_handler = StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    console_format = ColorFormatter(
        "%(levelname)s:     %(message)s"
    )
    console_handler.setFormatter(console_format)
    return console_handler

def get_file_handler():
    file_handler = TimedRotatingFileHandler(
        settings.LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=settings.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    file_formatter = Formatter(
        "%(asctime)s - %(levelname)s:     %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    return file_handler
