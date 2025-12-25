# 🤖 IsItTrue - Project Structure v4.0

## Senior Python Developer Architecture

### Project Organization

```
isittruebot/
├── backend/                          # Python Flask backend
│   ├── app.py                        # Main Flask application factory
│   ├── config.py                     # Centralized configuration
│   ├── requirements.txt              # Python dependencies
│   │
│   ├── core/                         # Core business logic
│   │   └── __init__.py              # AI Agent & Request Processor
│   │
│   ├── api/                          # REST API endpoints
│   │   └── __init__.py              # API routes & handlers
│   │
│   ├── services/                     # External service integration
│   │   └── __init__.py              # Gemini AI service
│   │
│   ├── integrations/                 # Third-party integrations
│   │   └── telegram_bot.py          # Telegram bot implementation
│   │
│   ├── modules/                      # Legacy modules (maintained for compatibility)
│   │   ├── analyzer.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── web_tools.py
│   │
│   └── logs/                         # Application logs
│       └── app.log
│
├── frontend/                         # Web interface
│   ├── templates/                    # HTML templates
│   │   ├── index.html               # Main page
│   │   ├── dashboard.html           # Dashboard (optional)
│   │   ├── 404.html                 # 404 error page
│   │   └── 500.html                 # 500 error page
│   │
│   └── static/                       # Static files
│       ├── css/
│       │   └── style.css            # Modern responsive CSS
│       ├── js/
│       │   └── app.js               # Frontend logic
│       └── images/
│           └── logo.png
│
├── .env                              # Environment variables
├── .gitignore                        # Git ignore file
├── requirements.txt                  # Project dependencies
├── README.md                         # Project documentation
└── PROJECT_STRUCTURE.md              # This file
```

## Architecture Explanation

### 1. **Core Module** (`backend/core/__init__.py`)
- `AIAgent`: Request type detection and validation
- `RequestProcessor`: Format requests and responses
- **Purpose**: Reusable business logic shared by Web UI and Telegram Bot

### 2. **Services Module** (`backend/services/__init__.py`)
- `GeminiService`: Gemini AI integration with retry logic
- `AIResponseFormatter`: Format AI responses
- **Purpose**: Handle external API integration with error handling

### 3. **API Module** (`backend/api/__init__.py`)
- REST endpoints for web interface
- `/api/analyze` - Main analysis endpoint
- `/api/detect-type` - Request type detection
- `/api/health` - Health check
- **Purpose**: Expose AI capabilities as HTTP endpoints

### 4. **Configuration** (`backend/config.py`)
- Centralized settings management
- Different configs for dev/prod/testing
- System prompts for each AI mode
- **Purpose**: Single source of truth for configuration

### 5. **Frontend** (`frontend/`)
- Modern Bootstrap 5 responsive design
- Real-time analysis with loading states
- Error handling and user feedback
- **Purpose**: User-friendly web interface

## Key Features

### ✅ Fact-Checking
- Verify claims with verdicts (TRUE/FALSE/UNVERIFIABLE)
- Evidence-based analysis
- Source recommendations

### 🤖 AI Detection
- Identify AI-generated content
- Pattern recognition
- Confidence levels

### 💬 General Chat
- Answer any question
- Knowledge-based responses
- Helpful and friendly

## How to Run

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Create .env file with:
GOOGLE_API_KEY=your_api_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
FLASK_ENV=development
```

### 3. Start Flask Server
```bash
python app.py
```

### 4. Access Web Interface
```
http://localhost:5000
```

## API Endpoints

### POST /api/analyze
**Request:**
```json
{
    "text": "Is the Earth flat?",
    "request_type": "fact_check",
    "temperature": 0.7
}
```

**Response:**
```json
{
    "success": true,
    "result": "FALSE. The Earth is spherical...",
    "type": "fact_check",
    "timestamp": "2025-12-25T10:30:00",
    "model": "gemini-2.5-flash"
}
```

### GET /api/health
**Response:**
```json
{
    "status": "healthy",
    "service": "IsItTrue AI Agent",
    "version": "4.0",
    "timestamp": "2025-12-25T10:30:00"
}
```

### POST /api/detect-type
**Request:**
```json
{
    "text": "Is this AI-generated?"
}
```

**Response:**
```json
{
    "success": true,
    "detected_type": "ai_detection",
    "text_length": 23
}
```

## Telegram Integration

The Telegram bot uses the same `AIAgent` core logic:

```python
from core import AIAgent

# In telegram_bot.py
request_type = AIAgent.detect_request_type(user_message)
system_prompt = AIAgent.get_system_prompt(request_type, config.SYSTEM_PROMPTS)
```

## Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Invalid input
- **404**: Endpoint not found
- **500**: Server error
- **503**: Service unavailable (health check failed)

### Error Response Format
```json
{
    "success": false,
    "error": "Error message",
    "error_code": "ERROR_TYPE"
}
```

## Scalability Considerations

1. **Async Support**: Ready for async/await with FastAPI migration
2. **Load Balancing**: Stateless Flask app (can run multiple instances)
3. **Caching**: Can add Redis for response caching
4. **Database**: Ready for SQLAlchemy integration
5. **Rate Limiting**: Can add flask-limiter

## Security

- ✅ API key stored in .env (not in code)
- ✅ CORS enabled for web requests
- ✅ Input validation on all endpoints
- ✅ Error messages don't expose sensitive info
- ✅ File size limits enforced
- ✅ Request timeout protection

## Testing

```bash
# Run health check
curl http://localhost:5000/api/health

# Test analysis
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Is Python a snake?","request_type":"fact_check"}'
```

## Development Workflow

1. **Modify core logic** → Update `backend/core/__init__.py`
2. **Add API endpoint** → Update `backend/api/__init__.py`
3. **Change UI** → Update `frontend/templates/` or `frontend/static/`
4. **Update config** → Modify `backend/config.py`
5. **Test** → Use curl or web interface

## Performance Metrics

- **Average response time**: 5-10 seconds (API call)
- **Max file size**: 16MB
- **Max text length**: 5000 characters
- **Concurrent requests**: Depends on deployment

## Future Enhancements

- [ ] Database integration for conversation history
- [ ] User authentication system
- [ ] Advanced caching with Redis
- [ ] WebSocket for real-time updates
- [ ] Admin dashboard
- [ ] API rate limiting
- [ ] Multiple AI models support
- [ ] File upload and analysis
- [ ] Batch processing
- [ ] Analytics and reporting

---

**Version**: 4.0
**Last Updated**: December 25, 2025
**Maintainer**: Senior Python Developer
