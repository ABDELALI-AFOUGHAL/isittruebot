# -*- coding: utf-8 -*-
"""
IsItTrue Telegram Bot - Simple Version
Simplified implementation without event loop issues
Enhanced with multilingual support
"""

import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
import sys
from modules.analyzer import IsItTrueAnalyzer
from modules.logger import setup_logger
from modules.config import TELEGRAM_TOKEN
from modules.language_detector import LanguageDetector

logger = setup_logger(__name__)

# Greeting messages in different languages
GREETINGS = {
    'fr': "👋 Salut! Je suis **IsItTrue**.\n\nEnvoyez-moi:\n📰 Un lien ou un texte à vérifier\n📸 Une image (pour détecter l'IA ou vérifier le texte)\n🎤 Un audio (transcription + vérification)\n\nPropulsé par Gemini 2.5 Flash ⚡",
    'en': "👋 Hi! I'm **IsItTrue**.\n\nSend me:\n📰 A link or text to verify\n📸 An image (to detect AI or verify text)\n🎤 Audio (transcription + verification)\n\nPowered by Gemini 2.5 Flash ⚡",
    'es': "👋 ¡Hola! Soy **IsItTrue**.\n\nEnvíame:\n📰 Un enlace o texto para verificar\n📸 Una imagen (para detectar IA o verificar texto)\n🎤 Audio (transcripción + verificación)\n\nPotenciado por Gemini 2.5 Flash ⚡",
    'de': "👋 Hallo! Ich bin **IsItTrue**.\n\nSend mir:\n📰 Einen Link oder Text zum Überprüfen\n📸 Ein Bild (um KI zu erkennen oder Text zu überprüfen)\n🎤 Audio (Transkription + Überprüfung)\n\nBetrieben von Gemini 2.5 Flash ⚡",
    'it': "👋 Ciao! Sono **IsItTrue**.\n\nInviami:\n📰 Un link o testo da verificare\n📸 Un'immagine (per rilevare IA o verificare il testo)\n🎤 Audio (trascrizione + verifica)\n\nAlimentato da Gemini 2.5 Flash ⚡",
    'pt': "👋 Oi! Sou **IsItTrue**.\n\nEnvie-me:\n📰 Um link ou texto para verificar\n📸 Uma imagem (para detectar IA ou verificar texto)\n🎤 Áudio (transcrição + verificação)\n\nPotenciado por Gemini 2.5 Flash ⚡",
}

ERROR_MESSAGES = {
    'fr': "⚠️ Veuillez envoyer du texte, une image ou un audio",
    'en': "⚠️ Please send text, an image or audio",
    'es': "⚠️ Por favor, envíe texto, una imagen o audio",
    'de': "⚠️ Bitte senden Sie Text, ein Bild oder Audio",
    'it': "⚠️ Per favore invia testo, un'immagine o audio",
    'pt': "⚠️ Por favor, envie texto, imagem ou áudio",
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with language detection"""
    # Detect user language from their message
    user_text = update.message.text or ""
    lang_code, lang_name, _ = LanguageDetector.detect_language(user_text)
    
    # Default to French if language not in our list
    greeting = GREETINGS.get(lang_code, GREETINGS['fr'])
    
    logger.info(f"🌐 User language detected: {lang_name} ({lang_code})")
    
    await update.message.reply_text(greeting, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all messages with language detection"""
    chat_id = update.effective_chat.id
    user_msg = update.message
    
    try:
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

        text_content = user_msg.text or user_msg.caption or ""
        image_bytes = None
        audio_bytes = None
        
        # Detect user language from text
        lang_code, lang_name, _ = LanguageDetector.detect_language(text_content)
        logger.info(f"🌐 Message language: {lang_name} ({lang_code})")

        # Handle photos
        if user_msg.photo:
            loading_msg = "🧐 Analyse de l'image..." if lang_code == 'fr' else "🧐 Analyzing image..."
            await update.message.reply_text(loading_msg)
            photo_file = await user_msg.photo[-1].get_file()
            image_bytes = await photo_file.download_as_bytearray()

        # Handle audio
        elif user_msg.voice or user_msg.audio:
            processing_msg = "🎧 Traitement de l'audio..." if lang_code == 'fr' else "🎧 Processing audio..."
            await update.message.reply_text(processing_msg)
            audio_obj = user_msg.voice or user_msg.audio
            audio_file = await audio_obj.get_file()
            audio_bytes = await audio_file.download_as_bytearray()

        # Analyze
        if text_content or image_bytes or audio_bytes:
            response = await IsItTrueAnalyzer.process_input(
                user_text=text_content,
                image_data=image_bytes,
                audio_data=audio_bytes
            )
            
            logger.info(f"📤 Sending response in {lang_name}")
            
            # Split response if too long
            max_length = 4096
            if len(response) > max_length:
                for i in range(0, len(response), max_length):
                    await update.message.reply_text(response[i:i+max_length])
            else:
                await update.message.reply_text(response)
        else:
            error_msg = ERROR_MESSAGES.get(lang_code, ERROR_MESSAGES['fr'])
            await update.message.reply_text(error_msg)

    except Exception as e:
        logger.error(f"Error: {e}")
        error_response = f"❌ Erreur: {str(e)[:100]}"
        await update.message.reply_text(error_response)


def main():
    """Start bot"""
    logger.info("=" * 60)
    logger.info("🤖 IsItTrue Telegram Bot v2.1 (Multilingual)")
    logger.info("=" * 60)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", start_command))  # /help does the same
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_message))
    
    logger.info("✅ Bot initialized with multilingual support")
    logger.info("🌐 Supported languages: French, English, Spanish, German, Italian, Portuguese")
    logger.info("📡 Starting polling...")
    
    app.run_polling()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n🛑 Bot stopped")
    except Exception as e:
        logger.error(f"Critical error: {e}")
