# app/core/logging_config.py
import logging
from typing import Any

# This is the configuration dictionary for Python's logging module.
LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False, # Keep default loggers (like uvicorn's)
    
    # Define the format of your log messages
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    
    # Define where the log messages go (e.g., to the console)
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr", # Log to standard error
        },
    },
    
    # Define the loggers themselves
    "loggers": {
        "hapitron_riddle_api": { # The name of our application's logger
            "handlers": ["default"],
            "level": "INFO", # The minimum level of message to handle
            "propagate": False,
        },
        # You can also configure other loggers here, e.g., uvicorn or sqlalchemy
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# A simple function to get our application's logger
def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance for the application.
    
    Args:
        name (str): The name of the module getting the logger, e.g., __name__.
    
    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(f"yemoy-vote.{name}")