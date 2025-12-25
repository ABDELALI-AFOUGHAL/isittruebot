#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for IsItTrue API
Tests text, URL, image, and audio analysis
"""

import requests
import json
import base64
import time
from pathlib import Path

API_URL = "http://localhost:5000/api/analyze"
TIMEOUT = 30

def test_text_analysis():
    """Test plain text analysis"""
    print("\n" + "="*60)
    print("🧪 TEST 1: ANALYSE DE TEXTE")
    print("="*60)
    
    data = {
        "text": "La Terre est plate selon quelques études récentes."
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=TIMEOUT)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ Réponse: {result.get('result', 'Pas de réponse')[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_url_analysis():
    """Test URL analysis"""
    print("\n" + "="*60)
    print("🔗 TEST 2: ANALYSE D'URL")
    print("="*60)
    
    data = {
        "text": "Vérifiez cet article: https://www.wikipedia.org/wiki/Earth"
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=TIMEOUT)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ Réponse: {result.get('result', 'Pas de réponse')[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_greeting():
    """Test greeting/conversation"""
    print("\n" + "="*60)
    print("👋 TEST 3: CONVERSATION (Salutation)")
    print("="*60)
    
    data = {
        "text": "Bonjour! Ça va? C'est quoi ton rôle?"
    }
    
    try:
        response = requests.post(API_URL, json=data, timeout=TIMEOUT)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ Réponse: {result.get('result', 'Pas de réponse')[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_image_analysis():
    """Test image analysis with a simple test image"""
    print("\n" + "="*60)
    print("🖼️  TEST 4: ANALYSE D'IMAGE")
    print("="*60)
    
    # Create a simple test image (1x1 red pixel PNG)
    png_hex = "89504e470d0a1a0a0000000d494844520000000100000001" \
              "0806000000001f15c4890000000a49444154789c6300010000" \
              "050001000a00000190040000"
    
    try:
        image_bytes = bytes.fromhex(png_hex)
        image_b64 = base64.b64encode(image_bytes).decode()
        
        data = {
            "text": "Analyser cette image",
            "image": f"data:image/png;base64,{image_b64}"
        }
        
        response = requests.post(API_URL, json=data, timeout=TIMEOUT)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ Réponse: {result.get('result', 'Pas de réponse')[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_multilingual():
    """Test multilingual support"""
    print("\n" + "="*60)
    print("🌐 TEST 5: SUPPORT MULTILINGUE")
    print("="*60)
    
    tests = [
        ("en", "Is the Earth flat? Some people claim this."),
        ("es", "¿La Tierra es plana? Algunas personas lo afirman."),
        ("de", "Ist die Erde flach? Einige Menschen behaupten das."),
    ]
    
    for lang_code, text in tests:
        print(f"\n  Langue: {lang_code} - '{text[:40]}...'")
        data = {"text": text}
        
        try:
            response = requests.post(API_URL, json=data, timeout=TIMEOUT)
            result = response.json()
            response_text = result.get('result', 'No response')[:100]
            print(f"  ✅ Réponse: {response_text}...")
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
    
    return True


def test_health_check():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("❤️  TEST 0: HEALTH CHECK")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"✅ Serveur OK: {result}")
        return True
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 DÉBUT DES TESTS API IsItTrue")
    print("="*60)
    
    # Test health first
    if not test_health_check():
        print("\n❌ Le serveur n'est pas accessible!")
        exit(1)
    
    # Run tests
    results = []
    results.append(("Texte", test_text_analysis()))
    time.sleep(1)
    results.append(("URL", test_url_analysis()))
    time.sleep(1)
    results.append(("Salutation", test_greeting()))
    time.sleep(1)
    results.append(("Image", test_image_analysis()))
    time.sleep(1)
    results.append(("Multilingue", test_multilingual()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n{passed}/{total} tests réussis")
    
    print("\n✅ Tests terminés!\n")
