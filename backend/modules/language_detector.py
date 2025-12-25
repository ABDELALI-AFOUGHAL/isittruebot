# -*- coding: utf-8 -*-
"""
Language detection module for IsItTrue Bot
"""

from langdetect import detect, LangDetectException
import logging

logger = logging.getLogger(__name__)

# Mapping des codes de langue ISO vers noms complets
LANGUAGE_NAMES = {
    'fr': 'Français',
    'en': 'Anglais',
    'es': 'Espagnol',
    'de': 'Allemand',
    'it': 'Italien',
    'pt': 'Portugais',
    'nl': 'Néerlandais',
    'ru': 'Russe',
    'ja': 'Japonais',
    'zh-cn': 'Chinois (Simplifié)',
    'zh-tw': 'Chinois (Traditionnel)',
    'ar': 'Arabe',
    'hi': 'Hindi',
    'tr': 'Turc',
    'pl': 'Polonais',
    'uk': 'Ukrainien',
    'ko': 'Coréen',
    'vi': 'Vietnamien',
    'th': 'Thaï',
    'sv': 'Suédois',
    'no': 'Norvégien',
    'da': 'Danois',
    'fi': 'Finnois',
    'cs': 'Tchèque',
    'ro': 'Roumain',
    'hu': 'Hongrois',
    'el': 'Grec',
}

# Instructions de réponse par langue
LANGUAGE_INSTRUCTIONS = {
    'fr': "Réponds TOUJOURS en Français. Tu es en France, parle comme un français!",
    'en': "Always respond in English. You are addressing English speakers!",
    'es': "Responde SIEMPRE en Español. ¡Estás hablando con hispanohablantes!",
    'de': "Antworte IMMER auf Deutsch. Du sprichst mit Deutschen!",
    'it': "Rispondi SEMPRE in Italiano. Stai parlando con italiani!",
    'pt': "Responda SEMPRE em Português. Você está falando com falantes de português!",
    'ar': "رد دائماً بالعربية. أنت تتحدث مع الناطقين بالعربية!",
    'ja': "常に日本語で返答してください。日本語を話す人々と話しています!",
    'zh-cn': "始终用中文回复。您正在与中文使用者交谈!",
    'ru': "Всегда отвечайте на русском языке. Вы говорите с русскоговорящими!",
    'ko': "항상 한국어로 답변하세요. 한국어를 사용하는 사람들과 대화하고 있습니다!",
}


class LanguageDetector:
    """Détecteur de langue pour IsItTrue"""
    
    @staticmethod
    def detect_language(text):
        """
        Détecte la langue du texte fourni.
        
        Args:
            text (str): Texte à analyser
            
        Returns:
            tuple: (code_langue, nom_langue, instruction)
        """
        if not text or len(text.strip()) < 3:
            # Par défaut, français
            return 'fr', 'Français', LANGUAGE_INSTRUCTIONS.get('fr', '')
        
        try:
            lang_code = detect(text)
            lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
            instruction = LANGUAGE_INSTRUCTIONS.get(lang_code, 
                                                   f"Respond in {lang_name}.")
            
            logger.info(f"🌐 Langue détectée: {lang_name} ({lang_code})")
            return lang_code, lang_name, instruction
            
        except LangDetectException as e:
            logger.warning(f"Impossible de détecter la langue: {e}")
            # Fallback au français
            return 'fr', 'Français', LANGUAGE_INSTRUCTIONS.get('fr', '')
        except Exception as e:
            logger.error(f"Erreur lors de la détection: {e}")
            return 'fr', 'Français', LANGUAGE_INSTRUCTIONS.get('fr', '')
    
    @staticmethod
    def get_instruction_for_language(lang_code):
        """
        Obtient l'instruction pour répondre dans une langue donnée.
        
        Args:
            lang_code (str): Code ISO de la langue
            
        Returns:
            str: Instruction pour Gemini
        """
        return LANGUAGE_INSTRUCTIONS.get(lang_code, 
                                        f"Respond in {LANGUAGE_NAMES.get(lang_code, 'the user language')}.")
