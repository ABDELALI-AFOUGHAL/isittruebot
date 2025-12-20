# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 22:07:45 2025

@author: NB
"""

import logging
import asyncio
import datetime
import re
import io
import os
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from duckduckgo_search import DDGS
import google.generativeai as genai
import trafilatura
from PIL import Image
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# ==========================================
# ⚙️ CONFIGURATION DU BOT
# ==========================================
TELEGRAM_TOKEN = "8466385633:AAGvO_-cydfhqUhBoei5lxD2xZW1Wqmo2B4" 
GEMINI_API_KEY = "AIzaSyBe0aZmGkXszybixlfzE63UBkqf9jr5Ef4" 


# Configuration de l'IA avec la clé
genai.configure(api_key=GEMINI_API_KEY)

# 🚀 UTILISATION DU MODÈLE GEMINI 2.5 FLASH (Visible sur ta capture)
# Ce modèle est multimodal : il voit, écoute et lit très vite.
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Configuration des logs (pour voir les erreurs dans le terminal)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# 🛠️ FONCTIONS OUTILS (RECHERCHE & EXTRACTION)
# ==========================================

def extract_url_content(text):
    """
    Détecte un lien URL, télécharge la page et extrait le texte principal.
    """
    if not text: return None, None
    
    # Regex pour trouver http ou https
    url_match = re.search(r'(https?://\S+)', text)
    if not url_match: return None, None

    url = url_match.group(0)
    logger.info(f"📄 Lien détecté, tentative de lecture : {url}")
    
    try:
        # Trafilatura est excellent pour ignorer les pubs et menus
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            article_text = trafilatura.extract(downloaded)
            if article_text:
                # On limite la taille pour ne pas saturer le prompt (env. 2000 mots)
                return url, article_text[:10000]
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du lien : {e}")
    
    return url, None

def search_web(query):
    """
    Recherche sur DuckDuckGo avec un filtre 'actualité récente' (1 semaine).
    """
    if not query or len(query.split()) < 2: return ""
    
    # Nettoyage de la requête
    clean_query = query[:200].replace("\n", " ")
    logger.info(f"🔍 Recherche Web lancée pour : {clean_query}")
    
    try:
        with DDGS() as ddgs:
            # timelimit='w' force les résultats de la semaine passée
            results = ddgs.text(clean_query, max_results=5, timelimit='w')
            if not results: return ""
            
            context = "--- RÉSULTATS RECHERCHE WEB RÉCENTS ---\n"
            for r in results:
                context += f"• Source: {r['title']}\n  Extrait: {r['body']}\n  Lien: {r['href']}\n\n"
            return context
    except Exception as e:
        logger.error(f"Erreur DuckDuckGo: {e}")
        return ""

# ==========================================
# 🧠 CERVEAU CENTRAL (PROMPT ENGINEER)
# ==========================================

async def analyze_multimodal_content(user_text=None, image_data=None, audio_data=None, url_found=None, web_context=""):
    today = datetime.date.today().strftime("%d %B %Y")
    
    prompt_parts = []
    
    # --- 1. LE CERVEAU ADAPTATIF (Nouveau Prompt) ---
    system_instruction = f"""
    Tu es "IsItTrue", un assistant IA à deux facettes. Nous sommes le {today}.

    TA PREMIÈRE MISSION EST DE DÉTECTER L'INTENTION DE L'UTILISATEUR :

    🟢 CAS 1 : CONVERSATION / SALUTATION (Ex: "Salut", "Ça va ?", "Merci", "Qui es-tu ?")
    -> Comportement : Sois amical, bref, chaleureux et parfois drôle. 
    -> INTERDIT : N'utilise PAS de format "Verdict" ou "Sources". Parle naturellement comme un humain sur Telegram.

    🔴 CAS 2 : VÉRIFICATION D'INFO (Ex: Une rumeur, un lien, une image politique, une affirmation douteuse)
    -> Comportement : Active ton mode "Fact-Checker Expert".
    -> Structure requise :
       - 🏳️ VERDICT : (Vrai / Faux / Trompeur / Non Prouvé / IA détectée)
       - 🧐 ANALYSE : Explication claire et factuelle.
       - 📚 SOURCES : Liste les liens trouvés dans le contexte web (si disponibles).
    """
    prompt_parts.append(system_instruction)

    # --- CAS IMAGE ---
    if image_data:
        task = """
        [CONTEXTE : L'utilisateur envoie une IMAGE]
        Si c'est une image personnelle ou drôle -> Réagis cool.
        Si c'est une image d'actualité ou suspecte -> Analyse-la (OCR + Détection Fake IA).
        """
        prompt_parts.append(task)
        img = Image.open(io.BytesIO(image_data))
        prompt_parts.append(img)
        if user_text: prompt_parts.append(f"Légende de l'image : {user_text}")

    # --- CAS AUDIO ---
    elif audio_data:
        task = """
        [CONTEXTE : L'utilisateur envoie un AUDIO]
        1. Transcris ce qui est dit.
        2. Si c'est juste un "Salut" -> Réponds au salut.
        3. Si c'est une affirmation -> Vérifie-la avec le contexte web.
        """
        prompt_parts.append(task)
        # Gestion fichier temp
        temp_filename = "temp_audio_msg.ogg"
        with open(temp_filename, "wb") as f:
            f.write(audio_data)
        uploaded_file = await asyncio.to_thread(genai.upload_file, path=temp_filename)
        prompt_parts.append(uploaded_file)

    # --- CAS TEXTE / URL ---
    elif user_text:
        if url_found:
            task = f"[CONTEXTE : LIEN DÉTECTÉ]\nContenu extrait du lien : {user_text}\n-> Analyse la véracité de cet article."
        else:
            task = f"[MESSAGE UTILISATEUR] : {user_text}"
        prompt_parts.append(task)

    # --- CONTEXTE WEB ---
    if web_context:
        prompt_parts.append(f"\n🔎 INFOS DU WEB (À utiliser seulement pour le CAS 2) :\n{web_context}")

    # --- GÉNÉRATION ---
    try:
        # On garde les safety settings au cas où
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        response = await model.generate_content_async(
            prompt_parts,
            generation_config=genai.types.GenerationConfig(temperature=0.4),
            safety_settings=safety_settings
        )
        return response.text
        
    except Exception as e:
        # AFFICHE L'ERREUR RÉELLE DANS TELEGRAM
        logger.error(f"ERREUR CRITIQUE GEMINI : {e}")
        return f"⚠️ ERREUR TECHNIQUE : {str(e)}\n\n(Envoie-moi une capture de ce message pour qu'on corrige !)"

# ==========================================
 # 📨 HANDLERS TELEGRAM
# ==========================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    Fonction maître qui reçoit TOUT (Texte, Photo, Audio) et aiguille.
    """
    chat_id = update.effective_chat.id
    user_msg = update.message
    
    # Feedback immédiat
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    # Variables pour le contenu
    text_content = user_msg.text or user_msg.caption # Caption = texte sous une photo
    image_bytes = None
    audio_bytes = None
    web_context = ""
    url_found = None
    article_content = None

    # 1. GESTION PHOTOS
    if user_msg.photo:
        await context.bot.send_message(chat_id=chat_id, text="🧐 J'analyse l'image...")
        # Récupérer la plus grande version
        photo_file = await user_msg.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()

    # 2. GESTION AUDIO
    elif user_msg.voice or user_msg.audio:
        await context.bot.send_message(chat_id=chat_id, text="🎧 J'écoute l'audio...")
        audio_obj = user_msg.voice or user_msg.audio
        audio_file = await audio_obj.get_file()
        audio_bytes = await audio_file.download_as_bytearray()

    # 3. GESTION TEXTE / LIEN (Si pas d'audio)
    else:
        # Si c'est du texte pur, on regarde s'il y a un lien
        url_found, content = extract_url_content(text_content)
        if url_found:
            await context.bot.send_message(chat_id=chat_id, text=f"📄 Je lis l'article : {url_found} ...")
            # Si on a trouvé un article, c'est ça le "texte" principal à analyser
            article_content = content 
        else:
            # Sinon c'est juste une question
            article_content = text_content

        # RECHERCHE WEB (Seulement utile pour le texte/liens pour l'instant)
        query = article_content[:200] if article_content else text_content
        if query:
            # On lance la recherche en tâche de fond (thread) pour ne pas bloquer
            loop = asyncio.get_running_loop()
            web_context = await loop.run_in_executor(None, search_web, query)

    # 4. APPEL FINAL AU CERVEAU
    # Si on a extrait un article, on l'envoie comme "user_text"
    final_text_input = article_content if article_content else text_content
    
    response = await analyze_multimodal_content(
        user_text=final_text_input,
        image_data=image_bytes,
        audio_data=audio_bytes,
        url_found=url_found,
        web_context=web_context
    )

    # 5. ENVOI RÉPONSE
    await context.bot.send_message(chat_id=chat_id, text=response)

# ==========================================
# 🏁 MAIN
# ==========================================

if __name__ == '__main__':
    print("🚀 Bot IsItTrue (Gemini 2.5) en cours de démarrage...")
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Commandes
    application.add_handler(CommandHandler("start", start_command))
    
    # Handler unique intelligent : il capture Texte, Photo ET Audio
    # filters.ALL capture tout sauf les commandes
    application.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_message))
    
    print("✅ Bot en ligne ! Prêt.")
    application.run_polling()