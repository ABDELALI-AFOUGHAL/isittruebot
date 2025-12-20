# -*- coding: utf-8 -*-
"""
Logger module for IsItTrue Bot
"""

import logging
from modules.config import LOG_LEVEL

def setup_logger(name):
    """Setup and return a logger instance"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=LOG_LEVEL
    )
    return logging.getLogger(name)
