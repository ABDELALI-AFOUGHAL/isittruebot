# -*- coding: utf-8 -*-
"""
Flask API for IsItTrue Web Interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import asyncio
import logging
from modules.analyzer import IsItTrueAnalyzer
from modules.logger import setup_logger
from modules.config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

logger = setup_logger(__name__)

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
CORS(app)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
async def analyze():
    """
    API endpoint for analysis
    Expects JSON with: text, image (base64), or audio (base64)
    """
    try:
        data = request.get_json()
        user_text = data.get('text', '').strip()
        image_data = data.get('image')
        audio_data = data.get('audio')

        if not user_text and not image_data and not audio_data:
            return jsonify({'error': 'Veuillez fournir du texte, une image ou un audio'}), 400

        logger.info("🔄 Analyse lancée...")
        
        # Decode base64 if needed
        image_bytes = None
        audio_bytes = None
        
        if image_data:
            import base64
            try:
                image_bytes = base64.b64decode(image_data.split(',')[1])
            except Exception as e:
                logger.error(f"Erreur décodage image: {e}")
        
        if audio_data:
            import base64
            try:
                audio_bytes = base64.b64decode(audio_data.split(',')[1])
            except Exception as e:
                logger.error(f"Erreur décodage audio: {e}")

        # Process through analyzer
        response = await IsItTrueAnalyzer.process_input(
            user_text=user_text,
            image_data=image_bytes,
            audio_data=audio_bytes
        )

        return jsonify({'result': response}), 200

    except Exception as e:
        logger.error(f"Erreur API: {e}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    print("🚀 IsItTrue Web Server - Démarrage...")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
