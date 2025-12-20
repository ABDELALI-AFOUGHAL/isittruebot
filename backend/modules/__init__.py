# -*- coding: utf-8 -*-
"""
IsItTrue Backend Modules
"""

from .config import *
from .logger import *
from .analyzer import *
from .web_tools import *

__all__ = [
    'IsItTrueAnalyzer',
    'extract_url_content',
    'search_web',
    'setup_logger',
]
