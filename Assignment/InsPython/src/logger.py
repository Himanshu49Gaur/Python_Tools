import logging
import os
import re
import sys
from typing import Optional

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bot.log")

class RedactSensitiveFilter(logging.Filter):
    """
    Logging filter that sanitizes sensitive API keys and HMAC signatures from log records.
    """
    def __init__(self, name: str = ""):
        super().__init__(name)
        # Regex patterns for key/signature parameters
        self.patterns = [
            (re.compile(r'(signature=)[a-fA-F0-9]{64}'), r'\1[REDACTED_SIGNATURE]'),
            (re.compile(r'(X-MBX-APIKEY:\s*)[^\s,]+'), r'\1[REDACTED_API_KEY]'),
            (re.compile(r'("api_key"|\'api_key\'|api_key=)[^\s,&]+'), r'\1[REDACTED_KEY]'),
            (re.compile(r'("api_secret"|\'api_secret\'|api_secret=)[^\s,&]+'), r'\1[REDACTED_SECRET]'),
        ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for pattern, replacement in self.patterns:
                record.msg = pattern.sub(replacement, record.msg)
        return True

def setup_logger(name: str = "binance_bot", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up and returns a structured logger writing to bot.log and stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    redact_filter = RedactSensitiveFilter()

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(redact_filter)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(redact_filter)
    logger.addHandler(console_handler)

    return logger

# Singleton default logger
logger = setup_logger()
