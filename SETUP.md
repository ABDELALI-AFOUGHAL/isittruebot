# IsItTrue - Installation & Setup Guide

## 🎯 What You Have

Your IsItTrue application now has:

1. **Restructured Backend** - Clean, modular Python code
2. **Beautiful Web Interface** - Modern HTML/CSS design
3. **Flask API** - Connects frontend to AI
4. **Telegram Bot** - For message-based usage
5. **Full Documentation** - README with examples

## 📦 Project Structure

```
isittruebot/
├── backend/
│   ├── modules/
│   │   ├── config.py       ← Configuration & secrets
│   │   ├── logger.py       ← Logging setup
│   │   ├── web_tools.py    ← URL extraction & search
│   │   └── analyzer.py     ← Core Gemini AI logic
│   ├── app.py              ← Flask web server
│   └── telegram_bot.py     ← Telegram bot entry point
├── frontend/
│   ├── index.html          ← Web interface
│   ├── css/style.css       ← Beautiful design system
│   └── js/app.js           ← Interactive features
├── requirements.txt        ← Python packages
├── .env.example            ← Configuration template
└── README.md              ← Full documentation
```

## 🚀 How to Run

### Option 1: Web Interface Only (Easiest)

```bash
# 1. Navigate to project
cd c:\Users\NB\isittruebot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up .env file
copy .env.example .env
# Edit .env and add your API keys

# 5. Run the server
cd backend
python app.py
```

Then open **http://localhost:5000** in your browser.

### Option 2: With Telegram Bot

```bash
cd backend
python telegram_bot.py
```

## 🔑 Getting API Keys

### Google Gemini API Key
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create new project if needed
4. Copy API key to `.env`

### Telegram Bot Token
1. Open Telegram app
2. Search for @BotFather
3. Send /newbot
4. Follow instructions
5. Copy token to `.env`

## 📝 Example .env File

```
TELEGRAM_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
GEMINI_API_KEY=AIzaSyD1234_ABCDEFghIjklmnop1234567890
LOG_LEVEL=INFO
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
```

## 🎨 Frontend Features You Get

✨ **Modern Design**
- Gradient backgrounds
- Smooth animations
- Professional color scheme

📱 **Responsive**
- Desktop (1920px+)
- Tablet (768px-1024px)
- Mobile (320px-767px)

🎯 **Easy to Use**
- Tab-based navigation
- Drag & drop image upload
- Real-time audio recording
- Loading states & error handling

## 📊 What Each File Does

### Backend Modules

**config.py**
- Stores API keys and settings
- Loads from `.env` file
- Prevents hardcoded secrets

**logger.py**
- Sets up logging for debugging
- Shows what's happening in console

**web_tools.py**
- `extract_url_content()` - Reads articles from URLs
- `search_web()` - Searches DuckDuckGo for recent news

**analyzer.py**
- `IsItTrueAnalyzer` - Main class
- `analyze_multimodal_content()` - Calls Gemini AI
- `process_input()` - Handles text/image/audio

**app.py**
- Flask web server
- `/` - Serves the web interface
- `/api/analyze` - Processes requests
- `/api/health` - Health check

**telegram_bot.py**
- Telegram bot implementation
- Reuses analyzer.py for logic

### Frontend Files

**index.html**
- Main interface structure
- Tabs for different input types
- Result display area

**css/style.css**
- Beautiful, modern design (600+ lines)
- Responsive breakpoints
- Animations & transitions

**js/app.js**
- Handles tab switching
- File uploads & recording
- API communication
- User feedback (loading, errors)

## 🔧 Customization

### Change Colors
Edit `frontend/css/style.css` root variables:
```css
:root {
    --primary: #6366f1;      /* Main purple */
    --secondary: #10b981;    /* Green */
    --danger: #ef4444;       /* Red */
    /* ... */
}
```

### Modify AI Behavior
Edit `backend/modules/analyzer.py`:
```python
system_instruction = f"""
Tu es "IsItTrue", un assistant IA...
# Customize the prompt here
"""
```

### Add New Features
Add endpoint in `backend/app.py`:
```python
@app.route('/api/new-feature', methods=['POST'])
async def new_feature():
    # Your code here
    return jsonify({'result': response})
```

## 📚 Key Improvements from Original

| Original | Now |
|----------|-----|
| Everything in one file | Organized modules |
| Hardcoded API keys | Environment variables |
| Telegram only | Web + Telegram |
| No styling | Beautiful UI |
| Manual testing | Ready to use |
| No documentation | Full README |

## 🐛 Troubleshooting

**"ModuleNotFoundError"**
- Install requirements: `pip install -r requirements.txt`

**"API Key Error"**
- Check `.env` file exists and has correct keys
- No extra spaces or quotes

**"Port already in use"**
- Change FLASK_PORT in `.env` to different number
- Or: `python app.py --port 5001`

**"No internet"**
- Web search won't work (but text analysis will)
- Check your internet connection

## 📞 Next Steps

1. ✅ Set up `.env` with your API keys
2. ✅ Install dependencies
3. ✅ Run the web server
4. ✅ Test in browser
5. ✅ Deploy to server (optional)

## 🚀 Deployment

For production, use:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

Or deploy to:
- Heroku
- Railway
- Render
- AWS
- DigitalOcean

---

**Enjoy using IsItTrue! 🎉**
