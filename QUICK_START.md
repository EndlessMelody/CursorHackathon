# ⚡ Quick Start Guide

## ✅ Current Status

**Frontend:** ✅ Running on http://localhost:3000

**Backend:** ⚠️ Needs to be started manually

## 🚀 Start the Backend

Open a **NEW terminal/PowerShell window** and run:

```powershell
# Navigate to project
cd C:\Users\HP\Cursor_Hackathon\CursorHackathon\backend

# Set your AI provider (FREE options available!)
# Option 1: Groq (FREE & FAST - Recommended!)
$env:GROQ_API_KEY="gsk-your-key-here"
$env:AI_PROVIDER="groq"

# Option 2: OpenAI (Paid)
# $env:OPENAI_API_KEY="sk-your-key-here"
# $env:AI_PROVIDER="openai"

# See FREE_AI_MODELS.md for all options!

# Start the server
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🎮 Play the Game

1. **Open your browser:** http://localhost:3000

2. **You should see:**
   - Character stats (Level, HP, XP, AC)
   - Narrative panel
   - Action input at the bottom

3. **Try these actions:**
   - `"attack the goblin"` - Combat with dice rolls
   - `"search the room"` - Skill check
   - `"move north"` - Movement (may encounter monsters)
   - `"rest"` - Heal HP
   - `"examine the door"` - Creative actions

## ⚠️ Important Notes

- **AI Provider is REQUIRED** - But you can use **FREE options**! 🆓
  - **Recommended:** Groq (FREE, fast, easy) - See `FREE_AI_MODELS.md`
  - **Other free options:** Ollama (local), Hugging Face, Together AI
  - **Paid option:** OpenAI - See `GET_API_KEY.md`
- Both servers must be running (backend on 8000, frontend on 3000)
- The backend handles all game rules (dice, combat, etc.)
- The AI only generates narrative/story descriptions

## 🐛 Troubleshooting

**Backend won't start?**
- Check if port 8000 is in use: `netstat -an | findstr 8000`
- Verify Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**Frontend won't load?**
- Check if it's running: `netstat -an | findstr 3000`
- Restart: `cd frontend && npm run dev`

**API errors?**
- Verify API key is set correctly
- Check you have API credits on your OpenAI account

## 📝 What's Running

- ✅ Frontend: http://localhost:3000 (Vite dev server)
- ⚠️ Backend: http://localhost:8000 (needs to be started)

Enjoy your adventure! 🗡️

