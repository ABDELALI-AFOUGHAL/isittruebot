# -*- coding: utf-8 -*-
"""
Web extraction and search tools for IsItTrue Bot
"""

import re
import logging
import trafilatura
from duckduckgo_search import DDGS
from modules.config import MAX_URL_CONTENT, MAX_QUERY_LENGTH

logger = logging.getLogger(__name__)


def extract_url_content(text):
    """
    Détecte un lien URL, télécharge la page et extrait le texte principal.
    Supporte les protocoles http et https.
    
    Args:
        text (str): Text potentially containing a URL
        
    Returns:
        tuple: (url, content) or (None, None) if no URL found
    """
    if not text or not isinstance(text, str):
        return None, None
    
    # Regex pour trouver http ou https URLs
    url_match = re.search(r'(https?://[^\s]+)', text)
    if not url_match:
        logger.debug(f"Pas d'URL trouvée dans: {text[:50]}")
        return None, None

    url = url_match.group(0).rstrip('.,;:!?\'"')  # Nettoie les caractères finaux
    logger.info(f"📄 URL détectée: {url}")
    
    try:
        # Trafilatura est excellent pour ignorer les pubs, menus, etc.
        logger.info(f"⏳ Téléchargement de {url}...")
        downloaded = trafilatura.fetch_url(url, timeout=10)
        
        if not downloaded:
            logger.warning(f"❌ Impossible de télécharger {url}")
            return url, None
        
        # Extraction du texte principal
        article_text = trafilatura.extract(downloaded)
        
        if not article_text:
            logger.warning(f"❌ Pas de contenu extractible de {url}")
            return url, None
        
        # Limite la taille pour ne pas saturer le prompt
        content = article_text[:MAX_URL_CONTENT]
        logger.info(f"✅ Contenu extrait: {len(content)} caractères")
        return url, content
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la lecture de {url}: {str(e)}")
        return url, None


def search_web(query):
    """
    Recherche sur DuckDuckGo avec un filtre 'actualité récente' (1 semaine).
    
    Args:
        query (str): Search query
        
    Returns:
        str: Formatted search results
    """
    if not query or len(query.split()) < 2:
        return ""
    
    # Nettoyage de la requête
    clean_query = query[:MAX_QUERY_LENGTH].replace("\n", " ")
    logger.info(f"🔍 Recherche Web lancée pour : {clean_query}")
    
    try:
        with DDGS() as ddgs:
            # timelimit='w' force les résultats de la semaine passée
            results = ddgs.text(clean_query, max_results=5, timelimit='w')
            if not results:
                return ""
            
            context = "--- RÉSULTATS RECHERCHE WEB RÉCENTS ---\n"
            for r in results:
                context += f"• Source: {r['title']}\n  Extrait: {r['body']}\n  Lien: {r['href']}\n\n"
            return context
    except Exception as e:
        logger.error(f"Erreur DuckDuckGo: {e}")
        return ""
