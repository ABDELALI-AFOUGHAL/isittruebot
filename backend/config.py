# -*- coding: utf-8 -*-
"""
Configuration centrale du projet IsItTrue
Senior Python Developer - Professional Configuration
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent.parent
BACKEND_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / 'frontend'

# ==================== API CONFIGURATION ====================

# Support both naming conventions
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ==================== FLASK CONFIGURATION ====================

class Config:
    """Base configuration"""
    # Flask settings
    JSON_ENSURE_ASCII = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Templates and static files
    TEMPLATE_FOLDER = str(FRONTEND_DIR / 'templates')
    STATIC_FOLDER = str(FRONTEND_DIR / 'static')
    STATIC_URL_PATH = '/static'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # API timeout
    REQUEST_TIMEOUT = 30
    
    # AI Model
    AI_MODEL = 'gemini-2.5-flash'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'INFO'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 'DEBUG'


# Get active config
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')

if ENVIRONMENT == 'production':
    active_config = ProductionConfig()
elif ENVIRONMENT == 'testing':
    active_config = TestingConfig()
else:
    active_config = DevelopmentConfig()


# ==================== LOGGING CONFIGURATION ====================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': active_config.LOG_LEVEL,
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': active_config.LOG_LEVEL,
            'formatter': 'detailed',
            'filename': str(BASE_DIR / 'logs' / 'app.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'root': {
        'level': active_config.LOG_LEVEL,
        'handlers': ['console', 'file']
    }
}


# ==================== SYSTEM PROMPTS ====================

SYSTEM_PROMPTS = {
    'fact_check': """You are a professional fact-checker AI.

For the user's claim, analyze and provide:
1. **Verdict**: TRUE / FALSE / UNVERIFIABLE / PARTIALLY TRUE
2. **Explanation**: 2-3 sentences explaining your reasoning
3. **Key Evidence**: 2-3 supporting points or sources if available
4. **Confidence Level**: HIGH / MEDIUM / LOW

Be concise, accurate, and objective. Cite reliable sources when possible.""",

    'ai_detection': """You are an AI detection specialist.

Analyze the provided text and determine if it was written by AI or a human.

Provide:
1. **Assessment**: LIKELY AI / LIKELY HUMAN / UNCLEAR
2. **Key Indicators**: 2-3 specific characteristics that led to your conclusion
3. **Confidence Level**: HIGH / MEDIUM / LOW
4. **Explanation**: 1-2 sentences explaining your analysis

Focus on patterns, writing style, and structural elements.""",

    'general_chat': """You are a helpful, friendly, and knowledgeable AI assistant.

Answer the user's question or respond to their input in a clear, concise manner.
- Be accurate and informative
- Use simple language when possible
- Provide examples if helpful
- Be honest about limitations or uncertainties"""
}


# ==================== VALIDATION SETTINGS ====================

VALIDATION = {
    'min_text_length': 1,
    'max_text_length': 5000,
    'allowed_file_types': ['jpg', 'jpeg', 'png', 'gif'],
    'max_file_size': 16 * 1024 * 1024,  # 16MB
}


# ==================== TELEGRAM SETTINGS ====================

TELEGRAM_CONFIG = {
    'polling_timeout': 30,
    'max_retries': 3,
    'retry_delay': 5,
}


# Ensure logs directory exists
(BASE_DIR / 'logs').mkdir(exist_ok=True)
