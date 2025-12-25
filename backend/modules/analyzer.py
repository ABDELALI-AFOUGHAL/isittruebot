# -*- coding: utf-8 -*-
"""
Core analysis module for IsItTrue Bot using Gemini AI
"""

import io
import asyncio
import datetime
import logging
import google.generativeai as genai
from PIL import Image
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from modules.config import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE
from modules.web_tools import extract_url_content, search_web
from modules.language_detector import LanguageDetector

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


class IsItTrueAnalyzer:
    """Main analyzer class for fact-checking"""
    
    @staticmethod
    async def analyze_multimodal_content(user_text=None, image_data=None, 
                                        audio_data=None, url_found=None, 
                                        web_context=""):
        """
        Analyze content using Gemini AI with multimodal support.
        Enhanced with language detection and multilingual responses.
        """
        # Detect language from user input
        detected_lang_code, detected_lang_name, lang_instruction = 'fr', 'Français', ''
        if user_text:
            detected_lang_code, detected_lang_name, lang_instruction = LanguageDetector.detect_language(user_text)
        
        today = datetime.date.today().strftime("%d %B %Y")
        prompt_parts = []
        
        # Enhanced system instruction with language support
        system_instruction = f"""Tu es "IsItTrue" 🔍, un assistant IA intelligent et multilingue. Aujourd'hui : {today}

┌─ 🌐 DIRECTIVE LINGUISTIQUE ─────────────────────┐
│ Langue détectée: {detected_lang_name}               │
│ {lang_instruction}     │
│ Emojis = oui, Texte = {detected_lang_name}       │
└─────────────────────────────────────────────────┘

┌─ MISSION CRITIQUE ─────────────────────────────────────┐
│ 1️⃣  DÉTECTE L'INTENTION (conversation vs fact-check)  │
│ 2️⃣  ADAPTE TA RÉPONSE EN FONCTION                      │
│ 3️⃣  SOIS PRÉCIS, COURTOIS ET ENGAGEANT                │
│ 4️⃣  RÉPONDS EN {detected_lang_name.upper()}                       │
└────────────────────────────────────────────────────────┘

🟢 TYPE 1 : SALUTATIONS & CONVERSATIONS
→ RÉACTION : Sois amical, chaleureux, avec humour parfois 😊
→ PARLE NATURELLEMENT EN {detected_lang_name.upper()}

🔴 TYPE 2 : VÉRIFICATION D'INFORMATIONS
→ STRUCTURE FIXE (EN {detected_lang_name.upper()}):
   🏳️  VERDICT : [Vrai ✓ / Faux ✗ / Trompeur ⚠️ / Non Prouvé ? / IA détectée 🤖]
   🧐 ANALYSE : Explication claire (2-3 phrases max)
   📚 SOURCES : Cite les liens pertinents du web
   💡 CONSEIL : Conseil pratique si utile

🟡 TYPE 3 : QUESTIONS SUR MOI
→ RÉACTION : Courte présentation personnelle en {detected_lang_name.upper()}

RÈGLES ABSOLUES :
✅ RÉPONDS TOUJOURS EN {detected_lang_name.upper()}
✅ Sois concis mais complet  
✅ Utilise des emojis pour clarifier
✅ Si tu ne sais pas = Dis-le honnêtement
❌ JAMAIS de réponses vagues"""
        
        prompt_parts.append(system_instruction)

        # Handle image
        if image_data:
            logger.info(f"📸 Image détectée: {len(image_data)} bytes")
            task = f"[📸 IMAGE REÇUE] Réponds en {detected_lang_name}"
            prompt_parts.append(task)
            
            try:
                img = Image.open(io.BytesIO(image_data))
                logger.info(f"✅ Image ouverte: {img.format} {img.size}")
                prompt_parts.append(img)
            except Exception as e:
                logger.error(f"❌ Erreur ouverture image: {e}")
                prompt_parts.append(f"[Image non lisible: {str(e)}]")
            
            if user_text:
                prompt_parts.append(f"Contexte : {user_text}")

        # Handle audio
        elif audio_data:
            logger.info(f"🎤 Audio détecté: {len(audio_data)} bytes")
            task = f"[🎤 AUDIO REÇU] Transcris et réponds en {detected_lang_name}"
            prompt_parts.append(task)
            temp_filename = "temp_audio_msg.ogg"
            with open(temp_filename, "wb") as f:
                f.write(audio_data)
            logger.info(f"💾 Fichier audio temporaire créé")
            uploaded_file = await asyncio.to_thread(genai.upload_file, path=temp_filename)
            prompt_parts.append(uploaded_file)

        # Handle text / URL
        elif user_text:
            if url_found:
                task = f"[🔗 LIEN] Analyse en {detected_lang_name}: {user_text}"
            else:
                task = f"[💬 MESSAGE EN {detected_lang_name.upper()}] \"{user_text}\""
            prompt_parts.append(task)

        # Add web context
        if web_context:
            prompt_parts.append(f"[📰 CONTEXTE WEB]\n{web_context}\nRéponds en {detected_lang_name}")

        # Generate response with retry mechanism
        max_retries = 3
        retry_delay = 1  # Start with 1 second
        
        for attempt in range(max_retries):
            try:
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }

                response = await model.generate_content_async(
                    prompt_parts,
                    generation_config=genai.types.GenerationConfig(temperature=TEMPERATURE),
                    safety_settings=safety_settings
                )
                return response.text
                
            except Exception as e:
                error_str = str(e)
                logger.error(f"ERREUR GEMINI (Attempt {attempt+1}/{max_retries}): {error_str}")
                
                # Check if it's a quota error (429)
                if "429" in error_str or "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        logger.info(f"Quota limit reached. Retrying in {retry_delay}s...")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        # All retries exhausted
                        error_msgs = {
                            'fr': "Quota API atteint. Veuillez réessayer dans quelques minutes.",
                            'en': "API quota reached. Please try again in a few minutes.",
                            'es': "Cuota de API alcanzada. Intente de nuevo en unos minutos.",
                            'de': "API-Kontingent erreicht. Bitte versuchen Sie es in einigen Minuten erneut.",
                            'it': "Quota API raggiunta. Riprovare tra qualche minuto.",
                            'pt': "Cota da API atingida. Tente novamente em alguns minutos.",
                        }
                        return error_msgs.get(detected_lang_code, "API quota limit reached. Please try again later.")
                
                # For non-quota errors on last attempt
                if attempt == max_retries - 1:
                    error_msgs = {
                        'fr': f"Erreur: {error_str[:60]}. Réessayez!",
                        'en': f"Error: {error_str[:60]}. Try again!",
                        'es': f"Error: {error_str[:60]}. ¡Intenta de nuevo!",
                        'de': f"Fehler: {error_str[:60]}. Versuchen Sie erneut!",
                        'it': f"Errore: {error_str[:60]}. Riprova!",
                        'pt': f"Erro: {error_str[:60]}. Tente novamente!",
                    }
                    return error_msgs.get(detected_lang_code, f"Error: {error_str[:50]}")
                
                # Retry with exponential backoff for other errors
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2

    @staticmethod
    async def process_input(user_text=None, image_data=None, audio_data=None):
        """
        Main processing pipeline with improved content extraction.
        
        Args:
            user_text (str): User's text input
            image_data (bytes): Image data if provided
            audio_data (bytes): Audio data if provided
            
        Returns:
            str: Analysis result
        """
        image_bytes = image_data
        audio_bytes = audio_data
        web_context = ""
        url_found = None
        article_content = None

        # PRIORITÉ 1: Images + optional text
        if image_bytes:
            # Si y'a du texte avec l'image, on le passe comme contexte
            article_content = user_text if user_text else "Image à analyser"
            
            # Si le texte contient une URL, on essaie d'extraire le contexte
            if user_text:
                detected_url, url_content = extract_url_content(user_text)
                if detected_url:
                    url_found = detected_url
                    web_context = url_content if url_content else ""

        # PRIORITÉ 2: Audio (pas d'image)
        elif audio_bytes:
            article_content = user_text if user_text else "Audio à analyser"

        # PRIORITÉ 3: Text / URL (pas d'image ni audio)
        elif user_text:
            # Essaie de détecter une URL dans le texte
            url_found, url_content = extract_url_content(user_text)
            
            if url_found and url_content:
                # URL détectée et contenu extrait avec succès
                article_content = url_content
                logger.info(f"✅ Contenu URL extrait: {len(url_content)} caractères")
            else:
                # Pas d'URL ou pas pu extraire le contenu
                article_content = user_text
                if url_found:
                    # URL détectée mais contenu pas dispo, le dire à Gemini
                    web_context = f"[URL fournie mais contenu non accessible: {url_found}]"
            
            # Web search pour contextualiser (si pas déjà URL)
            if not url_found and article_content:
                query = article_content[:200]
                web_context = await asyncio.to_thread(search_web, query)
                logger.info(f"🔍 Web search lancée pour: {query[:50]}...")

        final_text_input = article_content if article_content else user_text
        
        logger.info(f"📤 Envoi à Gemini - Texte: {len(final_text_input) if final_text_input else 0}c, "
                   f"Image: {'OUI' if image_bytes else 'NON'}, "
                   f"Audio: {'OUI' if audio_bytes else 'NON'}")
        
        response = await IsItTrueAnalyzer.analyze_multimodal_content(
            user_text=final_text_input,
            image_data=image_bytes,
            audio_data=audio_bytes,
            url_found=url_found,
            web_context=web_context
        )
        
        return response
