# 🗡️ AI Dungeon Master

An immersive, web-based D&D-like game powered by AI storytelling and a code-based rule engine.

## ✨ Features

- 🤖 **AI-Powered Narrative**: OpenAI GPT-4 generates immersive story descriptions
- ⚔️ **Rule Engine**: All game mechanics (dice rolls, combat, skill checks) are handled by code
- 🎲 **D&D Mechanics**: Real dice rolling, ability scores, AC, HP, XP, and leveling
- 🎨 **Beautiful UI**: Immersive dark theme with smooth animations
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎮 **Freeform Actions**: Type anything you want to do in natural language
- 🚀 **Easy Setup**: One-click startup with .env configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- AI API key (see options below)

### One-Time Setup

1. **Copy the example environment file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. **Edit `.env` file and add your API key:**
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key-here
   ```
   
   Or use a free option:
   ```env
   AI_PROVIDER=groq
   GROQ_API_KEY=gsk-your-key-here
   ```

3. **Install dependencies:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   npm install
   ```

### Starting the Game

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Manual (if scripts don't work):**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Then open **http://localhost:3000** in your browser!

## 🔑 Getting API Keys

### Option 1: Groq (FREE - Recommended!)
1. Go to https://console.groq.com/
2. Sign up (no credit card needed)
3. Create API key
4. Add to `.env`: `GROQ_API_KEY=gsk-your-key` and `AI_PROVIDER=groq`

### Option 2: OpenAI (Paid)
1. Go to https://platform.openai.com/api-keys
2. Sign up and add payment method
3. Create API key
4. Add to `.env`: `OPENAI_API_KEY=sk-your-key` and `AI_PROVIDER=openai`

### Option 3: Other Free Options
See `.env.example` for Ollama, Hugging Face, and Together AI options.

## 🎮 How to Play

1. Open `http://localhost:3000` in your browser
2. Type your actions in natural language:
   - "attack the goblin"
   - "search the room"
   - "move north"
   - "climb the wall"
   - "rest and heal"
   - Or anything creative you can think of!

3. The AI will narrate what happens based on your actions
4. The rule engine handles all dice rolls, combat, and game mechanics
5. Watch your stats, level up, and explore the dungeon!

## 🏗️ Architecture

### Backend (`backend/app.py`)
- **FastAPI** server for REST API
- **Rule Engine**: Handles all game mechanics (dice, combat, skills)
- **AI Integration**: Generates narrative descriptions
- **Game State Management**: Tracks character, inventory, monsters, etc.
- **.env Configuration**: Loads API keys from `.env` file automatically

### Frontend (`frontend/`)
- **React** with Vite for fast development
- **Modern UI** with immersive dark theme
- **Real-time Updates**: Shows narrative, events, and game state
- **Responsive Design**: Works on all screen sizes

## 🎲 Game Mechanics

### Combat
- Attack rolls use d20 + strength modifier + proficiency
- Damage rolls use d6 + strength modifier
- Critical hits on natural 20
- AC determines hit chance

### Skill Checks
- Ability checks use d20 + ability modifier + proficiency
- Difficulty Class (DC) determines success
- Advantage can be granted for certain actions

### Character Progression
- Gain XP from defeating monsters
- Level up automatically when XP threshold is reached
- HP increases on level up
- Proficiency bonus increases with level

## 📁 Project Structure

```
.
├── .env                    # Your API keys (create from .env.example)
├── .env.example            # Example configuration file
├── start.bat               # Windows startup script
├── start.sh                # Linux/Mac startup script
├── backend/
│   ├── app.py              # FastAPI server and game logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## 🔧 Configuration

### Using .env File (Recommended)

Create a `.env` file in the project root:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

The backend automatically loads this file on startup. No need to set environment variables manually!

### Backend
- Default port: `8000`
- Change in `app.py`: `uvicorn.run(app, host="0.0.0.0", port=8000)`

### Frontend
- Default port: `3000`
- API proxy configured in `vite.config.js`
- Change API base URL with environment variable: `VITE_API_BASE`

## 🎨 Customization

### Change Character Starting Stats
Edit `Character.__init__()` in `backend/app.py`

### Modify Rule Engine
All game rules are in the `RuleEngine` class in `backend/app.py`

### Customize AI Prompt
Edit the `get_dm_prompt()` function in `backend/app.py`

### Styling
Modify `frontend/src/App.css` for UI changes

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Check `.env` file exists and has valid API key

**Frontend won't start:**
- Check Node version: `node --version` (need 16+)
- Install dependencies: `npm install`
- Clear cache: `rm -rf node_modules && npm install`

**API errors:**
- Verify `.env` file has correct API key
- Check backend terminal for error messages
- Verify API key is valid and has credits

**Port already in use:**
- Backend: Change port in `app.py` or stop process using port 8000
- Frontend: Change port in `vite.config.js` or stop process using port 3000

## 📝 For Other Users

**To share this game with others:**

1. They only need to:
   - Copy `.env.example` to `.env`
   - Add their API key to `.env`
   - Run `start.bat` (Windows) or `./start.sh` (Linux/Mac)

2. That's it! No manual environment variable setup needed.

The `.env` file is in `.gitignore` so API keys won't be committed to git.

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Credits

Built with:
- FastAPI
- React
- Vite
- OpenAI GPT-4 / Groq
- Lots of imagination! 🎲
