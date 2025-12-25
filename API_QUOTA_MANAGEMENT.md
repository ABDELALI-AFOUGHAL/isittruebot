# API Quota Management Guide

## Problem: 429 Error - Quota Exceeded

When you see: `⚠️ Erreur: 429 You exceeded your current quota, please check your plan and billing details.`

This means the Gemini API has reached its quota limit.

## Root Causes

1. **Free Tier Quota**: Google Gemini API free tier has rate limits
   - ~60 requests per minute
   - ~1,500 requests per day
   - Resets daily at a specific time

2. **Billing Issues**: Subscription quota exceeded or payment problem

3. **High Concurrency**: Too many simultaneous requests

## Solutions

### Short-term (Immediate)

1. **Wait for quota reset** (usually within 24 hours)
2. **Implement retry with exponential backoff** ✅ DONE
   - Automatically retries failed requests
   - Waits 1s → 2s → 4s before each retry
   - Max 3 attempts per request

### Medium-term (Today)

1. **Check Gemini API quota**:
   ```bash
   # Visit: https://console.cloud.google.com/apis/dashboard
   # Look for: Google Generative AI API
   # Check: Usage and quotas section
   ```

2. **Upgrade to paid plan**:
   ```bash
   # Visit: https://aistudio.google.com/app/apikey
   # Click: "Check Usage" or upgrade billing
   ```

3. **Reduce request rate on frontend**:
   ```javascript
   // In frontend/static/js/app.js
   const ANALYZE_DEBOUNCE_MS = 1000;  // Wait 1s between requests
   ```

4. **Implement request caching** ✅ ALREADY DONE
   - Frontend caches results for identical inputs
   - Cache duration: 1 hour
   - Max cached results: 100

### Long-term (This Week)

1. **Use alternative API**: Consider Claude API, OpenAI, etc.

2. **Add request throttling**:
   ```python
   # In backend/modules/config.py
   MAX_REQUESTS_PER_MINUTE = 50
   DAILY_QUOTA = 1000
   ```

3. **Implement database storage**:
   - Store results for common queries
   - Reduce redundant API calls

4. **Monitor API usage**:
   - Add analytics dashboard
   - Track requests per hour
   - Alert when approaching quota

## Current Implementation

### Retry Mechanism (New)
Located in: `backend/modules/analyzer.py`

```python
max_retries = 3
retry_delay = 1  # seconds

for attempt in range(max_retries):
    try:
        response = await model.generate_content_async(...)
        return response.text
    except Exception as e:
        if "429" in error_str or "quota" in error_str.lower():
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
```

### User Messages (by Language)

**French**: "Quota API atteint. Veuillez réessayer dans quelques minutes."
**English**: "API quota reached. Please try again in a few minutes."
**Spanish**: "Cuota de API alcanzada. Intente de nuevo en unos minutos."
**German**: "API-Kontingent erreicht. Bitte versuchen Sie es in einigen Minuten erneut."
**Italian**: "Quota API raggiunta. Riprovare tra qualche minuto."
**Portuguese**: "Cota da API atingida. Tente novamente em alguns minutos."

## Testing Quota Limits

Test command to simulate quota limit:
```bash
# Send multiple requests rapidly
for i in {1..10}; do
    curl -X POST http://localhost:5000/api/analyze \
        -H "Content-Type: application/json" \
        -d '{"text":"Is the Earth flat?"}'
    echo "Request $i sent"
done
```

## Monitoring

### Check Request Logs
```bash
# Frontend error console
F12 → Console tab

# Backend logs
# Check terminal where Flask is running
# Look for: "ERREUR GEMINI" lines
```

### Track API Usage
Visit: https://console.cloud.google.com/apis/dashboard
- Quota usage graph
- Rate limit resets
- Error rates

## Environment Configuration

In `.env` file:
```
GEMINI_API_KEY=your_key_here
RETRY_ATTEMPTS=3
RETRY_DELAY=1
```

## Related Files

- `backend/modules/analyzer.py` - Core error handling
- `backend/app.py` - Flask error handlers
- `frontend/static/js/app.js` - Client-side error display
- `backend/modules/config.py` - Configuration
- `backend/modules/logger.py` - Logging setup

## When to Contact Support

Contact Google Cloud Support if:
1. Quota doesn't reset after 24 hours
2. You're on paid plan but quota still exceeded
3. Consistent 429 errors despite retries
4. API key appears to be invalid

Support: https://cloud.google.com/support

---

**Last Updated**: After implementing exponential backoff retry mechanism
**Status**: ✅ Automatic retry with backoff implemented
**Next**: Monitor quota usage and upgrade plan if needed
