# 🔑 Quick API Setup Guide

## The game is stuck because no API key is set!

### 🆓 Option 1: Groq (FREE - Recommended!)

**Step 1:** Get your free API key
- Go to: https://console.groq.com/
- Sign up (no credit card required!)
- Click "API Keys" → "Create API Key"
- Copy the key (starts with `gsk_`)

**Step 2:** Set the environment variables
```powershell
$env:GROQ_API_KEY="gsk-your-actual-key-here"
$env:AI_PROVIDER="groq"
```

**Step 3:** Restart the backend
- Stop the current backend (Ctrl+C in the terminal running it)
- Start it again: `cd backend && python app.py`

**That's it!** The game will now work with AI-generated narratives.

---

### 💰 Option 2: OpenAI (Paid)

**Step 1:** Get your API key
- Go to: https://platform.openai.com/api-keys
- Sign up and add payment method
- Create API key
- Copy the key (starts with `sk-`)

**Step 2:** Set the environment variable
```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
$env:AI_PROVIDER="openai"
```

**Step 3:** Restart the backend
- Stop the current backend (Ctrl+C)
- Start it again: `cd backend && python app.py`

---

## ⚡ Quick Test

After setting the API key and restarting, test it:
```powershell
# Test the backend
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
```

Then refresh your browser at http://localhost:3000

---

## 🆘 Troubleshooting

**Still stuck?**
1. Make sure you restarted the backend after setting the API key
2. Check the backend terminal for error messages
3. Verify the API key is correct (no extra spaces)
4. For Groq, make sure you set both `GROQ_API_KEY` and `AI_PROVIDER='groq'`

**Want to see what's happening?**
- Check the backend terminal - it will show API errors if the key is wrong
- Open browser console (F12) to see frontend errors

