# -*- coding: utf-8 -*-
"""
IsItTrue Telegram Bot
Main entry point for the Telegram bot implementation
"""

import asyncio
import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# Import from restructured modules
import sys
sys.path.insert(0, 'backend')
from modules.analyzer import IsItTrueAnalyzer
from modules.logger import setup_logger
from modules.config import TELEGRAM_TOKEN

logger = setup_logger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Salut ! Je suis **IsItTrue**. \n\n"
        "Envoyez-moi :\n"
        "📰 Un lien ou un texte à vérifier\n"
        "📸 Une image (pour détecter si c'est une IA ou vérifier le texte)\n"
        "🎤 Un audio (je le transcris et je vérifie)\n\n"
        "Je suis propulsé par Gemini 2.5 Flash ⚡"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Master handler for all message types (Text, Photo, Audio)
    """
    chat_id = update.effective_chat.id
    user_msg = update.message
    
    # Immediate feedback
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    # Variables for content
    text_content = user_msg.text or user_msg.caption
    image_bytes = None
    audio_bytes = None

    # 1. HANDLE PHOTOS
    if user_msg.photo:
        await context.bot.send_message(chat_id=chat_id, text="🧐 J'analyse l'image...")
        photo_file = await user_msg.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()

    # 2. HANDLE AUDIO
    elif user_msg.voice or user_msg.audio:
        await context.bot.send_message(chat_id=chat_id, text="🎧 J'écoute l'audio...")
        audio_obj = user_msg.voice or user_msg.audio
        audio_file = await audio_obj.get_file()
        audio_bytes = await audio_file.download_as_bytearray()

    # 3. ANALYZE
    try:
        response = await IsItTrueAnalyzer.process_input(
            user_text=text_content,
            image_data=image_bytes,
            audio_data=audio_bytes
        )
        
        await context.bot.send_message(chat_id=chat_id, text=response)
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ ERREUR TECHNIQUE : {str(e)}"
        )


async def main():
    """Start the Telegram bot"""
    logger.info("🚀 IsItTrue Bot Starting...")
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_message))
    
    logger.info("✅ Bot is online and ready!")
    
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
