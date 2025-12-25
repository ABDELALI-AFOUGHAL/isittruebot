# -*- coding: utf-8 -*-
"""
API Routes Module
Senior Python Developer - RESTful API Design
"""

import logging
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify

from core import AIAgent, RequestProcessor
from services import GeminiService

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


def init_api(app, gemini_service: GeminiService, config):
    """Initialize API with services"""
    app.register_blueprint(api_bp)
    app.gemini_service = gemini_service
    app.config_obj = config


# ==================== PUBLIC ROUTES ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        is_healthy = app.gemini_service.health_check()
        
        return jsonify({
            'status': 'healthy' if is_healthy else 'unhealthy',
            'service': 'IsItTrue AI Agent',
            'version': '4.0',
            'timestamp': datetime.now().isoformat(),
            'ai_model': app.config_obj.AI_MODEL,
        }), 200 if is_healthy else 503
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Main analysis endpoint
    
    POST /api/analyze
    {
        "text": "string (required)",
        "request_type": "fact_check|ai_detection|general_chat (optional)",
        "image": "base64 string (optional)",
        "temperature": "float 0-1 (optional, default: 0.7)"
    }
    """
    try:
        # Get JSON data
        data = request.get_json() or {}
        
        # Extract and validate text
        is_valid, result = AIAgent.validate_input(data.get('text', ''))
        if not is_valid:
            logger.warning(f"Invalid input: {result}")
            return jsonify({
                'success': False,
                'error': result
            }), 400
        
        text = result
        
        # Get optional parameters
        request_type = data.get('request_type')
        temperature = float(data.get('temperature', 0.7))
        image_data = data.get('image')  # Optional image data
        
        logger.info(f"📊 Analyze request: text_len={len(text)}, type={request_type}")
        
        # Auto-detect request type if not specified
        if not request_type:
            request_type = AIAgent.detect_request_type(text)
            logger.info(f"🔍 Auto-detected type: {request_type}")
        
        # Validate request type
        if request_type not in app.config_obj.SYSTEM_PROMPTS:
            request_type = 'general_chat'
        
        # Get system prompt
        system_prompt = app.config_obj.SYSTEM_PROMPTS.get(request_type)
        
        # Generate response from Gemini
        logger.info(f"Calling Gemini AI ({request_type})...")
        ai_response = app.gemini_service.generate_response(
            prompt=text,
            system_prompt=system_prompt,
            temperature=temperature
        )
        
        # Format and return response
        response_data = RequestProcessor.format_response(
            result=ai_response,
            request_type=request_type,
            metadata={
                'timestamp': datetime.now().isoformat(),
                'model': app.config_obj.AI_MODEL,
            }
        )
        
        logger.info(f"✅ Analysis complete: {request_type}")
        return jsonify(response_data), 200
    
    except ValueError as e:
        logger.warning(f"⚠️ Validation error: {e}")
        return jsonify(RequestProcessor.format_error(str(e), 'VALIDATION_ERROR')), 400
    
    except Exception as e:
        logger.error(f"❌ Analysis error: {e}", exc_info=True)
        return jsonify(RequestProcessor.format_error(
            f"Analysis failed: {str(e)[:100]}",
            'PROCESSING_ERROR'
        )), 500


@api_bp.route('/analyze', methods=['OPTIONS'])
def analyze_options():
    """Handle CORS preflight"""
    return '', 204


@api_bp.route('/detect-type', methods=['POST'])
def detect_type():
    """
    Detect request type without analyzing
    
    POST /api/detect-type
    {
        "text": "string"
    }
    """
    try:
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text required'
            }), 400
        
        detected_type = AIAgent.detect_request_type(text)
        
        return jsonify({
            'success': True,
            'detected_type': detected_type,
            'text_length': len(text)
        }), 200
    
    except Exception as e:
        logger.error(f"Type detection error: {e}")
        return jsonify(RequestProcessor.format_error(str(e))), 500


# ==================== ERROR HANDLERS ====================

@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'error_code': 'NOT_FOUND'
    }), 404


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'error_code': 'INTERNAL_ERROR'
    }), 500
