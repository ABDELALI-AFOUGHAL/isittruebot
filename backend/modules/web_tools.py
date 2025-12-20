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
    
    Args:
        text (str): Text potentially containing a URL
        
    Returns:
        tuple: (url, content) or (None, None) if no URL found
    """
    if not text:
        return None, None
    
    # Regex pour trouver http ou https
    url_match = re.search(r'(https?://\S+)', text)
    if not url_match:
        return None, None

    url = url_match.group(0)
    logger.info(f"📄 Lien détecté, tentative de lecture : {url}")
    
    try:
        # Trafilatura est excellent pour ignorer les pubs et menus
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            article_text = trafilatura.extract(downloaded)
            if article_text:
                # On limite la taille pour ne pas saturer le prompt
                return url, article_text[:MAX_URL_CONTENT]
    except Exception as e:
        logger.error(f"Erreur lors de la lecture du lien : {e}")
    
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
