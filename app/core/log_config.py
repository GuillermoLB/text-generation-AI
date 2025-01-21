import os
import logging
import logging.config
from pathlib import Path
from app.core.config import Settings

# Get log directory from environment variable with fallback
LOG_DIR = Path(os.getenv("APP_LOG_DIR", "var/log"))


def setup_logging():
    """Configure logging for the application"""
    # Create logs directory with proper permissions
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create log files if they don't exist
    log_file = LOG_DIR / "app.log"
    requests_file = LOG_DIR / "requests.log"

    for file in [log_file, requests_file]:
        file.touch(exist_ok=True)

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": str(log_file),
                "mode": "a",
            },
            "request_file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "formatter": "standard",
                "filename": str(requests_file),
                "mode": "a",
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True
            },
            "request_logger": {  # Request logger
                "handlers": ["request_file"],
                "level": "INFO",
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)
