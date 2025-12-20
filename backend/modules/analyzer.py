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
        
        Args:
            user_text (str): User's text input
            image_data (bytes): Image data if provided
            audio_data (bytes): Audio data if provided
            url_found (str): URL if detected
            web_context (str): Web search results context
            
        Returns:
            str: Analysis result
        """
        today = datetime.date.today().strftime("%d %B %Y")
        prompt_parts = []
        
        # System instruction
        system_instruction = f"""
    Tu es "IsItTrue", un assistant IA à deux facettes. Nous sommes le {today}.

    TA PREMIÈRE MISSION EST DE DÉTECTER L'INTENTION DE L'UTILISATEUR :

    🟢 CAS 1 : CONVERSATION / SALUTATION (Ex: "Salut", "Ça va ?", "Merci", "Qui es-tu ?")
    -> Comportement : Sois amical, bref, chaleureux et parfois drôle. 
    -> INTERDIT : N'utilise PAS de format "Verdict" ou "Sources". Parle naturellement.

    🔴 CAS 2 : VÉRIFICATION D'INFO (Ex: Une rumeur, un lien, une image politique, une affirmation douteuse)
    -> Comportement : Active ton mode "Fact-Checker Expert".
    -> Structure requise :
       - 🏳️ VERDICT : (Vrai / Faux / Trompeur / Non Prouvé / IA détectée)
       - 🧐 ANALYSE : Explication claire et factuelle.
       - 📚 SOURCES : Liste les liens trouvés dans le contexte web (si disponibles).
        """
        prompt_parts.append(system_instruction)

        # Handle image
        if image_data:
            task = """
        [CONTEXTE : L'utilisateur envoie une IMAGE]
        Si c'est une image personnelle ou drôle -> Réagis cool.
        Si c'est une image d'actualité ou suspecte -> Analyse-la (OCR + Détection Fake IA).
            """
            prompt_parts.append(task)
            img = Image.open(io.BytesIO(image_data))
            prompt_parts.append(img)
            if user_text:
                prompt_parts.append(f"Légende de l'image : {user_text}")

        # Handle audio
        elif audio_data:
            task = """
        [CONTEXTE : L'utilisateur envoie un AUDIO]
        1. Transcris ce qui est dit.
        2. Si c'est juste un "Salut" -> Réponds au salut.
        3. Si c'est une affirmation -> Vérifie-la avec le contexte web.
            """
            prompt_parts.append(task)
            temp_filename = "temp_audio_msg.ogg"
            with open(temp_filename, "wb") as f:
                f.write(audio_data)
            uploaded_file = await asyncio.to_thread(genai.upload_file, path=temp_filename)
            prompt_parts.append(uploaded_file)

        # Handle text / URL
        elif user_text:
            if url_found:
                task = f"[CONTEXTE : LIEN DÉTECTÉ]\nContenu extrait du lien : {user_text}\n-> Analyse la véracité de cet article."
            else:
                task = f"[MESSAGE UTILISATEUR] : {user_text}"
            prompt_parts.append(task)

        # Add web context
        if web_context:
            prompt_parts.append(f"\n🔎 INFOS DU WEB (À utiliser seulement pour le CAS 2) :\n{web_context}")

        # Generate response
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
            logger.error(f"ERREUR CRITIQUE GEMINI : {e}")
            return f"⚠️ ERREUR TECHNIQUE : {str(e)}"

    @staticmethod
    async def process_input(user_text=None, image_data=None, audio_data=None):
        """
        Main processing pipeline.
        
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

        # Handle text / URL extraction
        if user_text and not image_data and not audio_data:
            url_found, content = extract_url_content(user_text)
            if url_found:
                article_content = content
            else:
                article_content = user_text

            # Web search
            query = article_content[:200] if article_content else user_text
            if query:
                web_context = await asyncio.to_thread(search_web, query)

        final_text_input = article_content if article_content else user_text
        
        response = await IsItTrueAnalyzer.analyze_multimodal_content(
            user_text=final_text_input,
            image_data=image_bytes,
            audio_data=audio_bytes,
            url_found=url_found,
            web_context=web_context
        )
        
        return response
