# 🔍 IsItTrue - AI-Powered Fact Checker

**IsItTrue** is an advanced fact-checking application powered by Google's Gemini 2.5 Flash AI. It verifies information from text, URLs, images, and audio using intelligent analysis and web searches.

## ✨ Features

### 📝 Text Analysis
- Analyze rumors and statements for accuracy
- Intelligent context understanding
- Friendly or formal responses based on intent

### 🔗 URL Verification
- Automatically extract and analyze article content
- Verify credibility of sources
- Compare with recent web results

### 📸 Image Analysis
- Detect AI-generated images
- Extract and verify text from images (OCR)
- Analyze images for misinformation

### 🎤 Audio Processing
- Transcribe audio messages
- Verify spoken claims
- Extract and fact-check audio content

### 🧠 Intelligent Response System
- **CAS 1**: Friendly conversation (Salutations, casual chat)
- **CAS 2**: Expert fact-checking (Rumors, suspicious content)
  - 🏳️ VERDICT: True/False/Misleading/Unverified/AI-Detected
  - 🧐 ANALYSIS: Detailed explanation
  - 📚 SOURCES: Web references

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API Keys:
  - [Google Gemini API](https://ai.google.dev/)
  - [Telegram Bot Token](https://t.me/BotFather)

### Installation

1. **Clone the repository**
```bash
cd isittruebot
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

#### Web Interface Only
```bash
cd backend
python app.py
```
Then open `http://localhost:5000` in your browser.

#### With Telegram Bot
```bash
python version2_2.py
```

## 📁 Project Structure

```
isittruebot/
├── backend/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging setup
│   │   ├── web_tools.py       # URL extraction & web search
│   │   └── analyzer.py        # Core AI analysis
│   ├── app.py                 # Flask web server
│   └── version2_2.py          # Telegram bot (original)
├── frontend/
│   ├── index.html             # Main interface
│   ├── css/
│   │   └── style.css          # Modern design system
│   └── js/
│       └── app.js             # Frontend logic
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🎨 Frontend Features

- **Modern Design**: Gradient backgrounds, smooth animations
- **Responsive Layout**: Works on desktop, tablet, mobile
- **Intuitive Tabs**: Easy switching between input types
- **Real-time Feedback**: Loading states, error handling
- **Keyboard Shortcuts**: Ctrl/Cmd + Enter to analyze

## 🛠️ API Endpoints

### POST /api/analyze
Analyzes provided content.

**Request Body:**
```json
{
  "text": "Text to analyze",
  "image": "base64_encoded_image",
  "audio": "base64_encoded_audio"
}
```

**Response:**
```json
{
  "result": "Analysis result from Gemini AI"
}
```

### GET /api/health
Health check endpoint.

## 🔒 Security

- ✅ API keys stored in environment variables (`.env`)
- ✅ CORS enabled for web requests
- ✅ Input validation on all endpoints
- ✅ Safe harm filtering settings

## 📊 System Prompts

The AI uses adaptive prompts that detect user intent:

1. **Social Intent Detection**: Greeting, casual conversation
   - Response: Natural, friendly, brief
   
2. **Fact-Checking Intent**: Rumor verification, suspicious content
   - Response: Structured verdict with analysis and sources

## 🌐 Web Search Integration

- **DuckDuckGo API**: Recent news and articles
- **Trafilatura**: Clean content extraction
- **One-week timeframe**: Focuses on recent information

## 📱 Device Support

- ✅ Desktop (1920px+)
- ✅ Tablet (768px-1024px)
- ✅ Mobile (320px-767px)
- ✅ Print-friendly styles

## 🚀 Performance

- **Fast**: Gemini 2.5 Flash for quick analysis
- **Efficient**: Async processing for multiple requests
- **Lightweight**: Minimal CSS/JS dependencies
- **Responsive**: No lag on modern browsers

## 🐛 Troubleshooting

### "API Key Invalid"
- Check `.env` file for correct keys
- Verify keys haven't expired
- Ensure no extra spaces in `.env`

### "No microphone access"
- Grant browser permission to record audio
- Use HTTPS for better security (microphone requires it)

### "Web search failed"
- Check internet connection
- DuckDuckGo might be rate-limited (try again later)

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚠️ API Quota Management

The application includes **automatic retry mechanism with exponential backoff** for API quota limits (429 errors):

- **Automatic Retries**: Up to 3 attempts with delays (1s → 2s → 4s)
- **Rate Limit Detection**: Identifies quota errors specifically
- **User-Friendly Messages**: Errors in user's detected language
- **Frontend Caching**: Results cached for 1 hour to reduce API calls

### If You Get 429 Error
1. Wait a few minutes (quota resets daily)
2. Check your API plan at: https://aistudio.google.com/app/apikey
3. Upgrade to paid plan if needed
4. See `API_QUOTA_MANAGEMENT.md` for detailed solutions

### Monitor Your Usage
- Visit: https://console.cloud.google.com/apis/dashboard
- Check "Google Generative AI API" quotas
- Track daily request limits

## 📞 Support

Need help? Check:
- 📖 Inline code comments
- 🔍 Docstrings in Python modules
- 🎨 CSS class naming conventions
- 💬 GitHub Issues
- 📋 See `API_QUOTA_MANAGEMENT.md` for quota issues

## 🎯 Roadmap

- [ ] Database for analysis history
- [ ] User authentication
- [ ] Multi-language support
- [ ] Custom training data
- [ ] Integration with other fact-checking APIs
- [ ] Browser extension

---

**Made with ❤️ for Truth**  
Powered by Google Gemini 2.5 Flash ⚡
