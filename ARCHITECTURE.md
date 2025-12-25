# IsItTrue - Senior Python Architecture
**Version 2.3 - Refactored & Production-Ready**

---

## Project Structure

```
isittruebot/
├── backend/
│   ├── app.py                          # Flask app (refactored)
│   ├── telegram_bot_simple.py          # Telegram bot
│   ├── modules/
│   │   ├── analyzer.py                 # Core fact-checking logic
│   │   ├── language_detector.py        # Language detection
│   │   ├── web_tools.py                # Web extraction & search
│   │   ├── config.py                   # Configuration
│   │   ├── logger.py                   # Logging setup
│   │   └── __init__.py
│   └── requirements.txt                # Dependencies
│
├── frontend/
│   ├── templates/
│   │   └── index.html                  # Modern Bootstrap 5 interface
│   └── static/
│       ├── css/
│       │   └── style.css               # Dark mode custom CSS
│       └── js/
│           └── app.js                  # Frontend JavaScript
│
└── Documentation/
    ├── ARCHITECTURE.md                 # This file
    ├── API_DOCUMENTATION.md            # API endpoints
    └── DEPLOYMENT.md                   # Deployment guide
```

---

## Architecture Overview

### Separation of Concerns (DRY Principle)

**Core Logic (`modules/analyzer.py`)**
- All fact-checking logic lives in `IsItTrueAnalyzer` class
- Used by both Flask web app and Telegram bot
- No code duplication
- Single source of truth

**Flask Web Application (`app.py`)**
- Serves HTML/CSS/JS frontend
- Provides REST API (`/api/analyze`)
- Handles multimodal input (text, URL, image, audio)
- Error handling & validation

**Telegram Bot (`telegram_bot_simple.py`)**
- Imports `IsItTrueAnalyzer` directly
- Processes messages same way as web API
- Multilingual support built-in
- Async message handling

### Data Flow

```
User Input
    ↓
┌─────────────┬─────────────┐
│   Web App   │ Telegram Bot│
└─────────────┴─────────────┘
         ↓          ↓
     Flask    python-telegram-bot
         ↓          ↓
    Shared Core Logic
    IsItTrueAnalyzer.process_input()
         ↓
  Language Detection
  Content Analysis
  Gemini AI Processing
         ↓
    Response → User
```

---

## Technologies Used

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.13+ | Core language |
| Flask | 3.0.0+ | Web framework |
| Flask-CORS | Latest | Cross-origin support |
| google-generativeai | Latest | Gemini AI API |
| python-telegram-bot | 21.0.1+ | Telegram integration |
| trafilatura | 1.6.1+ | Web content extraction |
| duckduckgo-search | Latest | Web search API |
| langdetect | Latest | Language detection |
| python-dotenv | Latest | Environment variables |

### Frontend
| Technology | Purpose |
|-----------|---------|
| HTML5 | Markup |
| Bootstrap 5 | Responsive framework |
| Bootstrap Icons | Icons library |
| CSS3 | Dark mode styling |
| JavaScript ES6+ | Interactivity |

---

## Requirements.txt

```
# Web Framework
Flask==3.0.0
Flask-CORS==4.0.0

# AI & Language
google-generativeai>=0.3.0
langdetect>=1.0.9

# Web Tools
trafilatura>=1.6.1
duckduckgo-search>=3.9.0
requests>=2.31.0

# Telegram
python-telegram-bot==21.0.1

# Utilities
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

---

## Installation & Setup

### 1. Clone Repository
```bash
cd isittruebot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment (.env)
```bash
# .env file
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True

TELEGRAM_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_api_key_here

LOG_LEVEL=INFO
```

### 5. Run Backend API
```bash
cd backend
python app.py
# Server running at http://127.0.0.1:5000
```

### 6. Run Telegram Bot
```bash
cd backend
python telegram_bot_simple.py
# Bot polling for messages
```

---

## API Documentation

### POST /api/analyze
**Fact-checking analysis endpoint**

**Request:**
```json
{
  "text": "The Earth is flat. (optional)",
  "image": "data:image/png;base64,... (optional)",
  "audio": "data:audio/webm;base64,... (optional)"
}
```

**Response (Success):**
```json
{
  "result": "Verdict: False ✗\n\nAnalysis: Scientific evidence overwhelmingly proves...\n\nSources: NASA, ESA, ..."
}
```

**Response (Error):**
```json
{
  "error": "Please provide text, image, or audio for analysis"
}
```

### GET /api/health
**Health check endpoint**

**Response:**
```json
{
  "status": "ok",
  "service": "IsItTrue Fact-Checker",
  "version": "2.3"
}
```

---

## Code Examples

### Using Core Logic (Shared)

```python
from modules.analyzer import IsItTrueAnalyzer
import asyncio

# Both web app and Telegram bot use this same function
result = asyncio.run(
    IsItTrueAnalyzer.process_input(
        user_text="Is the Earth flat?",
        image_data=None,
        audio_data=None
    )
)
print(result)
```

### Flask Integration
```python
# app.py
from modules.analyzer import IsItTrueAnalyzer

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    response = asyncio.run(
        IsItTrueAnalyzer.process_input(
            user_text=data.get('text'),
            image_data=image_bytes,
            audio_data=audio_bytes
        )
    )
    return jsonify({'result': response})
```

### Telegram Bot Integration
```python
# telegram_bot_simple.py
from modules.analyzer import IsItTrueAnalyzer

async def handle_message(update, context):
    response = await IsItTrueAnalyzer.process_input(
        user_text=update.message.text,
        image_data=image_bytes,
        audio_data=audio_bytes
    )
    await update.message.reply_text(response)
```

---

## Features

✅ **Multimodal Input**
- Text analysis
- URL extraction & analysis
- Image OCR with Gemini
- Audio transcription

✅ **Multilingual Support**
- 30+ languages detected automatically
- Responses in user's language

✅ **Web Interface**
- Modern dark mode UI
- Responsive Bootstrap 5 design
- Real-time analysis
- Result caching

✅ **Telegram Bot**
- Telegram channel integration
- Same analysis logic as web
- Language-aware responses

✅ **Production Ready**
- Error handling
- Logging system
- CORS enabled
- Async/await architecture

---

## Development Best Practices

### 1. **DRY Principle**
- Core logic in `modules/analyzer.py`
- Reused by web and Telegram bot
- Changes affect all interfaces

### 2. **Error Handling**
- All APIs return proper status codes
- Error messages in user's language
- Logging for debugging

### 3. **Performance**
- Async/await for I/O operations
- Result caching (frontend)
- Request timeout handling

### 4. **Security**
- Input validation
- CORS enabled
- Environment variable configuration
- No API keys in code

---

## Deployment

### Development Server
```bash
cd backend
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install -r backend/requirements.txt
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

---

## Troubleshooting

### "Event loop is closed" error
- Solution: Update `app.py` to use `asyncio.run()`
- Located in `/api/analyze` endpoint

### Telegram bot not responding
- Check TELEGRAM_TOKEN in `.env`
- Verify bot token is correct
- Check internet connectivity

### API returns 404
- Ensure Flask app is running on port 5000
- Check frontend API_URL in `app.js`

---

## Future Enhancements

- [ ] Database for storing analysis history
- [ ] User authentication
- [ ] Advanced analytics dashboard
- [ ] Batch analysis API
- [ ] WebSocket for real-time updates
- [ ] Browser extension
- [ ] Mobile app (React Native)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.3 | 2025-12-25 | Senior refactoring, Bootstrap 5 UI |
| 2.2 | 2025-12-25 | Multilingual support for web |
| 2.1 | 2025-12-25 | Telegram bot multilingual |
| 2.0 | 2025-12-25 | Initial bot + web implementation |

---

## License & Credits

Built with ❤️ using Flask, Gemini AI, and Bootstrap

---

**Senior Python Developer Notes:**
- Architecture follows SOLID principles
- Single Responsibility for each module
- DRY principle maintained throughout
- Async/await for non-blocking I/O
- Proper error handling and logging
- Clean code, well-documented
