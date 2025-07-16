import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("centralized_logger")
    logger.setLevel(logging.DEBUG)
    # Create a file handler with rotation
    handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()