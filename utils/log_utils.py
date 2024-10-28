#utils/log_utils.py


import logging
import os

def setup_logging(log_level=None):
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "info").upper()
    
    logging.basicConfig(level=log_level)
    return logging.getLogger(__name__)
