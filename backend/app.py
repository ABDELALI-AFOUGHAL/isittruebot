# -*- coding: utf-8 -*-
"""
IsItTrue - Friendly AI Agent Backend
Senior Python Developer - Professional Architecture v4.0

Structure:
- core/        → AI Agent logic, request processing
- api/         → REST API endpoints
- services/    → Gemini AI integration
- integrations/ → Telegram, external services
- frontend/    → Web UI (templates, static files)
"""

import logging
import logging.config
from flask import Flask, render_template
from flask_cors import CORS
from pathlib import Path

# Import configuration and services
from config import active_config, LOGGING_CONFIG, SYSTEM_PROMPTS
from services import GeminiService
from api import init_api

# ==================== LOGGING SETUP ====================

# Create logs directory
logs_dir = Path(__file__).parent.parent / 'logs'
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# ==================== FLASK APPLICATION FACTORY ====================

def create_app(config=None):
    """
    Application factory for Flask
    
    Args:
        config: Configuration object (default: active_config)
        
    Returns:
        Configured Flask application
    """
    if config is None:
        config = active_config
    
    # Initialize Flask
    app = Flask(
        __name__,
        template_folder=str(config.TEMPLATE_FOLDER),
        static_folder=str(config.STATIC_FOLDER),
        static_url_path=config.STATIC_URL_PATH
    )
    
    # Apply configuration
    app.config.from_object(config)
    app.config_obj = config
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # ==================== SERVICE INITIALIZATION ====================
    
    # Initialize Gemini Service
    try:
        app.gemini_service = GeminiService(
            api_key=config.__dict__.get('GOOGLE_API_KEY') or __import__('config').GOOGLE_API_KEY,
            model=config.AI_MODEL
        )
    except ValueError as e:
        logger.error(f"[ERROR] Failed to initialize Gemini: {e}")
        raise
    
    # ==================== BLUEPRINT REGISTRATION ====================
    
    # Register API blueprints
    init_api(app, app.gemini_service, config)
    
    # ==================== ROUTE: WEB UI ====================
    
    @app.route('/')
    def index():
        """Serve main web interface"""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Serve dashboard"""
        return render_template('dashboard.html')
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {error}")
        return render_template('500.html'), 500
    
    @app.errorhandler(413)
    def request_too_large(error):
        """Handle file too large"""
        return {'error': 'Request payload too large'}, 413
    
    # ==================== STARTUP BANNER ====================
    
    with app.app_context():
        logger.info("=" * 70)
        logger.info("🤖 IsItTrue - Friendly AI Agent Backend v4.0")
        logger.info("=" * 70)
        logger.info(f"Environment: {__import__('config').ENVIRONMENT}")
        logger.info(f"Debug Mode: {app.debug}")
        logger.info(f"AI Model: {config.AI_MODEL}")
        logger.info("=" * 70)
        logger.info("🎯 Capabilities:")
        logger.info("  ✓ Fact-Checking")
        logger.info("  ✓ AI Detection")
        logger.info("  ✓ General Chat")
        logger.info("=" * 70)
        logger.info(f"📁 Templates: {config.TEMPLATE_FOLDER}")
        logger.info(f"📁 Static: {config.STATIC_FOLDER}")
        logger.info("=" * 70)
    
    return app


# ==================== APPLICATION ENTRY POINT ====================

# Create the application instance
app = create_app(active_config)

if __name__ == '__main__':
    # Run Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=active_config.DEBUG,
        use_reloader=active_config.DEBUG
    )

