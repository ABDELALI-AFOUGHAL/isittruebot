# 🔐 Upgrade API Key - Guide Complet

## Problème

```
Erreur 429: You exceeded your current quota
Free tier limit: 20 requests/day
Need: Unlimited requests
```

---

## Solutions (du plus simple au plus complet)

### ✅ Solution 1: Attendre le Reset (GRATUIT)
**Temps**: 24 heures  
**Coût**: €0

1. Attendre minuit (UTC) pour quota reset
2. Réessayer demain
3. **Limitation**: Toujours 20 requêtes/jour

### ✅ Solution 2: Upgrade Gratuit (GRATUIT)
**Temps**: 5-10 minutes  
**Coût**: €0 (1 mois gratuit)

1. Aller à: https://aistudio.google.com/app/apikey
2. Cliquer: "Enable billing" ou "Upgrade"
3. Ajouter payment method
4. Sélectionner: "Gemini API"
5. Quota augmente à: ~1000 requêtes/jour
6. **Gratuit**: Premier mois (crédits Google)

### ✅ Solution 3: Mode Production (PAYANT)
**Temps**: 15 minutes  
**Coût**: €1-50/mois (selon usage)

**Étapes complètes**:

#### 3.1 Créer Google Cloud Project
```
1. Aller à: https://console.cloud.google.com
2. Cliquer: "Create Project"
3. Nommer: "IsItTrue-Bot"
4. Région: Votre pays (ex: France)
5. Cliquer: "Create"
6. Attendre 1-2 minutes
```

#### 3.2 Activer Gemini API
```
1. En haut, chercher: "Generative AI API"
2. Cliquer: "Enable API"
3. Attendre activation (30 sec)
```

#### 3.3 Créer Service Account
```
1. Menu gauche: "Service Accounts"
2. Cliquer: "Create Service Account"
3. Nom: "isittruebot"
4. Cliquer: "Create and Continue"
5. Roles:
   ├─ Sélectionner: "Generative AI Editor"
   └─ Cliquer: "Continue"
6. Cliquer: "Done"
```

#### 3.4 Créer API Key
```
1. Cliquer sur: service account créé
2. Onglet: "Keys"
3. Cliquer: "Add Key" → "Create new key"
4. Format: "JSON"
5. Cliquer: "Create"
6. Fichier JSON téléchargé
7. **Garder CONFIDENTIEL!**
```

#### 3.5 Configurer Billing
```
1. Menu gauche: "Billing"
2. Lier project à compte billing
3. Ajouter payment method
4. Budget alert: €50/mois (optionnel)
```

---

## 📱 Mise à jour .env

### Avant (API Key simple)
```env
GEMINI_API_KEY=AIzaSyD...
```

### Après (Service Account)
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

Ou (API Key nouveau)
```env
GEMINI_API_KEY=AIzaSyD...  # Nouvelle clé avec quotas augmentés
```

---

## 🔄 Mettre à jour le Code

### Option 1: Utiliser nouvelle API Key (Simple)
```python
# Dans backend/modules/config.py
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Nouvelle clé
genai.configure(api_key=GEMINI_API_KEY)
```

### Option 2: Utiliser Service Account (Sécurisé)
```python
# Installer: pip install google-auth-httplib2
import google.auth
from google.auth.transport import requests

credentials, project = google.auth.default()
credentials.refresh(requests.Request())
```

---

## 📊 Quotas Comparaison

| Plan | Coût | Requêtes/jour | Requêtes/min | Support |
|------|------|---------------|--------------|---------|
| Free | €0 | 20 | 2 | Non |
| Gratuit+Billing | €0-15 | 1000 | 60 | Support |
| Production | €1-50 | Illimité | Illimité | Oui |

---

## 🧪 Test API Key

### Vérifier Quota Courant
```bash
cd backend
python -c "
import os
from google.generativeai import Client
import google.generativeai as genai

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# Check usage
print('API Key: ' + api_key[:20] + '...')
print('Status: Connected ✅')
"
```

### Tester une Requête
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Is the Earth flat?"}'
```

Expected: Réponse rapide ✅ ou "Quota reached" ❌

---

## 🛡️ Sécurité

### ⚠️ JAMAIS partager:
- ❌ API Keys
- ❌ Service account JSON
- ❌ Credentials

### ✅ Recommandations:
- 🔒 Utiliser `.env` (git ignored)
- 🔒 Variables d'environnement
- 🔒 Google Cloud Secrets Manager (production)
- 🔒 Rotation régulière des clés
- 🔒 Restrictions IP (Console Cloud)

---

## 📞 Support & Resources

### Oficial Links:
- 🔗 API Quotas: https://ai.google.dev/gemini-api/docs/rate-limits
- 🔗 Pricing: https://ai.google.dev/pricing
- 🔗 Docs: https://ai.google.dev/docs
- 🔗 Console: https://console.cloud.google.com

### Troubleshooting:
```
ERROR: "API key not valid"
→ Vérifier .env file
→ Redémarrer Flask

ERROR: "Project not set"
→ Créer Google Cloud Project
→ Activer Generative AI API
→ Relancer application

ERROR: "Still 429"
→ Attendre quota reset
→ Ou vérifier account billing
→ Ou utiliser nouvelle clé
```

---

## ⏱️ Temps Requis

| Action | Temps | Coût |
|--------|-------|------|
| Reset gratuit | 24h | €0 |
| Upgrade gratuit | 10 min | €0 |
| Production setup | 30 min | €1-50/mois |

---

## 🎯 Recommandation

**Pour développement**: 
→ Upgrade gratuit (1000 req/jour) ✅

**Pour production**:
→ Service Account + Billing (Illimité) ✅

---

**Prochaines étapes**:
1. Choisir solution (gratuit ou payant)
2. Obtenir nouvelle API key
3. Mettre à jour `.env`
4. Redémarrer Flask
5. Tester requête
6. Confirmation: Quota dépassé? NON ✅

