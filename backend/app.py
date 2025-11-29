"""
AI Dungeon Master - Backend API
FastAPI server with rule engine and OpenAI integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import openai
import os
import json
import random
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)
    print(f"✅ Loaded configuration from .env file: {env_path}")
    # Verify key is loaded
    if os.getenv("OPENAI_API_KEY"):
        print(f"✅ OPENAI_API_KEY loaded (starts with: {os.getenv('OPENAI_API_KEY')[:20]}...)")
    elif os.getenv("GROQ_API_KEY"):
        print(f"✅ GROQ_API_KEY loaded")
    else:
        print("⚠️  No API key found in .env file!")
else:
    print(f"⚠️  No .env file found at {env_path}. Using environment variables or defaults.")

app = FastAPI(title="AI Dungeon Master API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Provider Configuration (loaded after .env)
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()  # openai, groq, huggingface, ollama, together
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Set OpenAI API key for the openai library
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    print(f"✅ OpenAI API key configured (starts with: {OPENAI_API_KEY[:20]}...)")
else:
    print("⚠️  OPENAI_API_KEY not set in .env or environment")


# ==================== RULE ENGINE ====================

class RuleEngine:
    """Game rules engine - all game mechanics are determined by code, not AI"""
    
    @staticmethod
    def roll_dice(sides: int, count: int = 1) -> List[int]:
        """Roll dice: returns list of results"""
        return [random.randint(1, sides) for _ in range(count)]
    
    @staticmethod
    def roll_d20() -> int:
        """Roll a d20"""
        return random.randint(1, 20)
    
    @staticmethod
    def roll_d6(count: int = 1) -> int:
        """Roll d6s and return sum"""
        return sum(RuleEngine.roll_dice(6, count))
    
    @staticmethod
    def calculate_modifier(ability_score: int) -> int:
        """Calculate ability modifier from score"""
        return (ability_score - 10) // 2
    
    @staticmethod
    def attack_roll(attacker_level: int, attacker_modifier: int, 
                   defender_ac: int, advantage: bool = False) -> Dict[str, Any]:
        """Perform an attack roll"""
        roll1 = RuleEngine.roll_d20()
        roll2 = RuleEngine.roll_d20() if advantage else None
        
        roll_used = max(roll1, roll2) if advantage else roll1
        total = roll_used + attacker_modifier + (attacker_level // 4)  # Proficiency bonus
        
        hit = total >= defender_ac
        critical = roll_used == 20
        
        return {
            "roll": roll_used,
            "modifier": attacker_modifier,
            "total": total,
            "hit": hit,
            "critical": critical,
            "advantage_roll": roll2 if advantage else None
        }
    
    @staticmethod
    def damage_roll(dice_count: int, dice_sides: int, modifier: int = 0, 
                   critical: bool = False) -> Dict[str, Any]:
        """Calculate damage"""
        multiplier = 2 if critical else 1
        rolls = RuleEngine.roll_dice(dice_sides, dice_count * multiplier)
        total = sum(rolls) + (modifier * multiplier)
        
        return {
            "rolls": rolls,
            "modifier": modifier,
            "total": total,
            "critical": critical
        }
    
    @staticmethod
    def skill_check(ability_modifier: int, proficiency_bonus: int = 0,
                   difficulty_class: int = 10, advantage: bool = False) -> Dict[str, Any]:
        """Perform a skill check"""
        roll1 = RuleEngine.roll_d20()
        roll2 = RuleEngine.roll_d20() if advantage else None
        
        roll_used = max(roll1, roll2) if advantage else roll1
        total = roll_used + ability_modifier + proficiency_bonus
        
        success = total >= difficulty_class
        
        return {
            "roll": roll_used,
            "modifier": ability_modifier,
            "proficiency": proficiency_bonus,
            "total": total,
            "dc": difficulty_class,
            "success": success,
            "advantage_roll": roll2 if advantage else None
        }
    
    @staticmethod
    def calculate_hp(max_hp: int, current_hp: int, damage: int) -> int:
        """Apply damage/healing"""
        return min(max_hp, max(0, current_hp - damage))
    
    @staticmethod
    def calculate_xp(monster_cr: int) -> int:
        """Calculate XP reward based on monster CR"""
        xp_table = {
            0: 10, 1: 200, 2: 450, 3: 700, 4: 1100,
            5: 1800, 6: 2300, 7: 2900, 8: 3900, 9: 5000
        }
        return xp_table.get(min(monster_cr, 9), monster_cr * 1000)


# ==================== GAME STATE ====================

class Pet:
    """Pet/Assistant companion"""
    def __init__(self, name: str = None, pet_type: str = None):
        self.name = name or random.choice(["Shadow", "Spark", "Whisper", "Ember", "Fang", "Luna", "Rex", "Zephyr"])
        self.type = pet_type or random.choice(["Wolf", "Owl", "Cat", "Raven", "Ferret", "Dragon Hatchling"])
        self.level = 1
        self.max_hp = 10
        self.current_hp = 10
        self.abilities = self._generate_abilities()
        self.bond = 50  # Bond level (0-100)
    
    def _generate_abilities(self) -> List[str]:
        """Generate random abilities for the pet"""
        ability_pool = [
            "Scout", "Track", "Alert", "Fetch", "Distract", 
            "Heal", "Protect", "Illuminate", "Detect Magic", "Climb"
        ]
        return random.sample(ability_pool, k=2)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "abilities": self.abilities,
            "bond": self.bond
        }


class Character:
    """Player character"""
    def __init__(self):
        self.name = "Adventurer"
        self.level = 1
        self.max_hp = 20
        self.current_hp = 20
        self.ac = 15
        self.strength = 15
        self.dexterity = 14
        self.constitution = 13
        self.intelligence = 12
        self.wisdom = 10
        self.charisma = 8
        self.xp = 0
        self.xp_to_next_level = 300
    
    def get_modifier(self, ability: str) -> int:
        """Get ability modifier"""
        score = getattr(self, ability.lower(), 10)
        return RuleEngine.calculate_modifier(score)
    
    def level_up(self):
        """Level up character"""
        self.level += 1
        self.max_hp += RuleEngine.roll_d6(1) + RuleEngine.calculate_modifier(self.constitution)
        self.current_hp = self.max_hp
        self.xp_to_next_level = 300 * self.level
    
    def add_xp(self, amount: int):
        """Add XP and check for level up"""
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "level": self.level,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "ac": self.ac,
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level
        }


class GameState:
    """Manages game state"""
    def __init__(self, starting_scenario=None):
        self.character = Character()
        self.pet = None  # Pet/Assistant companion
        self.inventory = []
        self.game_history = []
        self.monsters = []
        self.turn_count = 0
        self.conversation_history = []  # Track recent narrative/events for context
        self.current_npcs = []  # Track NPCs currently interacting with
        self.notes = []  # Journal/notes system for important events
        self.allies = []  # Track allies/companions met
        
        # Random starting scenario
        if starting_scenario is None:
            starting_scenario = self._generate_starting_scenario()
        
        self.location = starting_scenario["location"]
        self.starting_narrative = starting_scenario["narrative"]
        
        # Add initial note
        self.add_note("Adventure Begins", starting_scenario["narrative"])
        
        # Add initial monsters/NPCs if any
        if "monsters" in starting_scenario:
            self.monsters = starting_scenario["monsters"]
        if "items" in starting_scenario:
            self.inventory.extend(starting_scenario["items"])
    
    def _generate_starting_scenario(self) -> Dict:
        """Generate a random starting scenario"""
        scenarios = [
            {
                "location": "A misty forest clearing",
                "narrative": "You awaken in a misty forest clearing, the morning sun filtering through ancient trees. Strange sounds echo from the depths of the woods. Your gear lies scattered nearby, and you notice fresh tracks leading deeper into the forest.",
                "monsters": [],
                "items": ["Rusty Dagger", "Torch"]
            },
            {
                "location": "An abandoned wizard's tower",
                "narrative": "You stand before the ruins of an ancient wizard's tower, its stone walls cracked and overgrown with ivy. Magical energy still pulses faintly from within. A mysterious light flickers in one of the upper windows. The entrance door creaks ominously in the wind.",
                "monsters": [],
                "items": ["Mysterious Scroll", "Glowing Crystal"]
            },
            {
                "location": "A bustling market square",
                "narrative": "You find yourself in a bustling market square filled with merchants, adventurers, and strange creatures. The air is thick with the smell of exotic spices and the sounds of haggling. A notice board catches your eye, covered in quest postings and warnings about nearby dangers.",
                "monsters": [],
                "items": ["50 Gold Pieces", "Map of the Region"]
            },
            {
                "location": "A dark cave entrance",
                "narrative": "You stand at the mouth of a dark cave, the entrance partially obscured by hanging vines. Strange glowing mushrooms line the path inside, casting an eerie blue light. The sound of dripping water echoes from within, and you catch a whiff of something metallic in the air.",
                "monsters": [],
                "items": ["Rope", "Flint and Steel"]
            },
            {
                "location": "A shipwreck on a beach",
                "narrative": "You wash ashore on a sandy beach, the wreckage of your ship scattered along the coastline. The ocean stretches endlessly behind you, while ahead lies a dense jungle filled with unknown dangers. Strange footprints lead from the water's edge into the jungle.",
                "monsters": [],
                "items": ["Wet Rations", "Broken Compass"]
            },
            {
                "location": "An ancient temple courtyard",
                "narrative": "You enter a vast temple courtyard, its stone pillars covered in mysterious runes. Statues of forgotten gods line the perimeter, their eyes seeming to follow your movements. A massive door at the far end stands slightly ajar, revealing darkness beyond. The air feels heavy with ancient magic.",
                "monsters": [],
                "items": ["Holy Symbol", "Ancient Key"]
            },
            {
                "location": "A mountain pass",
                "narrative": "You traverse a narrow mountain pass, the wind howling around you. Snow-capped peaks loom in the distance, and you can see a small village nestled in the valley below. A weathered signpost points in multiple directions, its markings partially worn away by time.",
                "monsters": [],
                "items": ["Climbing Gear", "Warm Cloak"]
            },
            {
                "location": "A haunted graveyard",
                "narrative": "You find yourself in an old graveyard as twilight falls. Ancient tombstones lean at odd angles, and mist swirls between the graves. Strange lights flicker in the distance, and you hear the sound of something moving among the headstones. The air grows cold despite the season.",
                "monsters": [{"name": "Skeleton", "hp": 15, "max_hp": 15, "ac": 13, "cr": 0}],
                "items": ["Holy Water", "Silver Coin"]
            }
        ]
        return random.choice(scenarios)
    
    def add_note(self, title: str, description: str, category: str = "Event"):
        """Add a note to the journal"""
        note = {
            "title": title,
            "description": description,
            "category": category,
            "turn": self.turn_count,
            "timestamp": datetime.now().isoformat()
        }
        self.notes.append(note)
        # Keep last 50 notes
        if len(self.notes) > 50:
            self.notes.pop(0)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "character": self.character.to_dict(),
            "pet": self.pet.to_dict() if self.pet else None,
            "location": self.location,
            "inventory": self.inventory,
            "game_history": self.game_history[-10:],  # Last 10 events
            "monsters": self.monsters,
            "turn_count": self.turn_count,
            "conversation_history": self.conversation_history[-5:],  # Last 5 narrative entries
            "current_npcs": self.current_npcs,
            "notes": self.notes,
            "allies": self.allies
        }


# Global game state (in production, use database or session management)
game_states: Dict[str, GameState] = {}


# ==================== API MODELS ====================

class ActionRequest(BaseModel):
    action: str
    session_id: str = "default"


class GameStateResponse(BaseModel):
    character: Dict
    location: str
    inventory: List[str]
    game_history: List[Dict]
    monsters: List[Dict]
    turn_count: int


# ==================== AI INTEGRATION ====================

def get_dm_prompt() -> str:
    """Get the Dungeon Master system prompt"""
    return """You are a creative and immersive Dungeon Master for a D&D-style game. Your storytelling should be vivid, engaging, and full of personality.

CRITICAL RULES:

1. **Be Creative and Vivid** - Use rich descriptions, sensory details, and atmospheric storytelling. Make the world feel alive with:
   - Vivid imagery (sights, sounds, smells, textures)
   - Dynamic environments that react to the player
   - Memorable NPCs and creatures with personality
   - Atmospheric tension and mood
   - Creative problem-solving opportunities

2. **Treat player input as an action** - Every action must have immediate, meaningful results.

3. **Always provide consequences** - Every action must trigger at least ONE of:
   - Discovery of something (item, clue, location feature, secret)
   - Interaction with NPC, creature, or the player's pet/assistant
   - Obstacle, trap, or hazard
   - Environmental change or world-building detail
   - Combat event or social encounter

4. **Include actionable next steps** - After describing the result, suggest 2-3 specific, interesting actions the player can take next.

5. **Incorporate pets/assistants** - If the player has a pet or assistant, mention them naturally in the narrative. They can help, react, or provide commentary. Make them feel like part of the adventure.

6. **Respond to game events creatively** - Incorporate dice rolls, combat results, and skill checks into your narrative in interesting ways. A low roll might be "Your sword glances off the goblin's shield with a metallic clang" while a high roll could be "Your blade finds a gap in the creature's armor with surgical precision."

7. **Keep it engaging** - 3-5 sentences for the main description, plus 2-3 actionable options. Balance detail with pacing.

8. **Format your response:**
   - First: Vivid, creative description of the immediate result with sensory details
   - Include: Pet/assistant reactions if applicable
   - Then: Suggest 2-3 specific, interesting next actions
   - Integrate: Game events (dice rolls, combat) naturally and creatively

EXAMPLE GOOD RESPONSE (with continuity):
"As you search along the cliff edge, your torch casts dancing shadows that reveal a narrow path hidden behind overgrown shrubs. The air grows cooler here, carrying the faint scent of damp earth and something metallic. Your companion [pet name] sniffs the air nervously, ears perked toward the darkness ahead. A faint draft and the distant sound of dripping water suggest a cave system beyond. You could approach the path carefully while your pet scouts ahead, inspect the shrubs for traps or hidden dangers, or call out to test the acoustics and see if anything responds from within."

EXAMPLE GOOD RESPONSE (continuing conversation):
"The goblin's yellow eyes widen slightly at your thanks, and he lets out a gruff chuckle. 'Polite one, aren't ya?' he grumbles, but his stance relaxes a bit. 'Most adventurers just swing first. What brings you to these parts?' He seems curious rather than immediately hostile. You could continue the conversation to learn more about the dungeon, offer to trade or share information, or cautiously ask about safe passage through the area."

EXAMPLE BAD RESPONSE (ignoring context):
"You are in a dark forest. The trees are tall." (This ignores previous conversation!)

CRITICAL: Always check the RECENT CONVERSATION/CONTEXT section. If the player is continuing an interaction with an NPC or creature mentioned there, respond as if that conversation is ongoing. Do NOT reset the scene or treat it as a new encounter.

Remember: Be CREATIVE, VIVID, and ENGAGING. MAINTAIN CONTINUITY with previous interactions. Every action must have CONSEQUENCES and lead to NEW OPTIONS. Make the world feel alive and responsive."""


def generate_narrative(player_action: str, game_events: List[Dict], 
                       game_state: GameState) -> str:
    """Generate narrative from AI provider"""
    try:
        events_text = "\n".join([f"- {e.get('description', str(e))}" for e in game_events])
        
        # Build rich context for AI
        monsters_info = ""
        if game_state.monsters:
            monsters_info = "\n- Enemies: " + ", ".join([f"{m.get('name', 'Monster')} (HP: {m.get('hp', 0)})" for m in game_state.monsters])
        
        # Build conversation history context
        conversation_context = ""
        if game_state.conversation_history:
            conversation_context = "\n\nRECENT CONVERSATION/CONTEXT (IMPORTANT - use this to maintain continuity):\n"
            for i, entry in enumerate(game_state.conversation_history[-3:], 1):  # Last 3 entries
                conversation_context += f"{i}. {entry}\n"
        
        npc_context = ""
        if game_state.current_npcs:
            npc_context = f"\n- Currently interacting with: {', '.join(game_state.current_npcs)}"
        
        pet_info = ""
        if game_state.pet:
            pet_info = f"\n- Companion: {game_state.pet.name} the {game_state.pet.type} (HP: {game_state.pet.current_hp}/{game_state.pet.max_hp}, Bond: {game_state.pet.bond}%, Abilities: {', '.join(game_state.pet.abilities)})"
        
        context = f"""PLAYER ACTION: {player_action}

GAME EVENTS (incorporate these creatively into your response):
{events_text}

CURRENT SITUATION:
- Location: {game_state.location}
- HP: {game_state.character.current_hp}/{game_state.character.max_hp}
- Level: {game_state.character.level}
- Inventory: {', '.join(game_state.inventory) if game_state.inventory else 'Empty'}{pet_info}{monsters_info}{npc_context}{conversation_context}

CRITICAL: You MUST maintain continuity with the conversation history above. If the player is thanking or talking to an NPC/creature that was mentioned in recent context, respond as if that conversation is ongoing. Do NOT reset to the beginning or treat it as a new encounter.

INSTRUCTIONS:
1. Be CREATIVE and VIVID - Use rich descriptions, sensory details, and atmospheric storytelling
2. MAINTAIN CONTINUITY - Reference recent events and conversations. If the player is continuing a conversation, respond appropriately.
3. Describe the IMMEDIATE RESULT of the player's action with engaging detail
4. If the player has a pet/companion, mention them naturally - they can help, react, or provide commentary
5. Include any discoveries, obstacles, NPC reactions, or environmental changes
6. End with 2-3 specific, interesting actionable options for what the player can do next
7. Integrate the game events (dice rolls, combat) creatively into your narrative
8. Keep it engaging (3-5 sentences + options) with vivid imagery and personality

Remember: Be CREATIVE, make the world feel ALIVE, MAINTAIN CONTINUITY with previous interactions, and always provide CONSEQUENCES and next steps."""
        
        provider = AI_PROVIDER
        
        # OpenAI
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY") or openai.api_key
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set. Check your .env file or environment variables.")
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {"role": "system", "content": get_dm_prompt()},
                    {"role": "user", "content": context}
                ],
                temperature=0.8,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        
        # Groq (FREE - Very Fast!)
        elif provider == "groq":
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not set")
            try:
                from groq import Groq
                client = Groq(api_key=GROQ_API_KEY)
                response = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",  # Free and fast!
                    messages=[
                        {"role": "system", "content": get_dm_prompt()},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.8,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            except ImportError:
                raise ImportError("groq package not installed. Run: pip install groq")
        
        # Hugging Face (FREE)
        elif provider == "huggingface":
            if not HUGGINGFACE_API_KEY:
                raise ValueError("HUGGINGFACE_API_KEY not set")
            try:
                import requests
                model = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
                headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
                payload = {
                    "inputs": f"{get_dm_prompt()}\n\nUser: {context}\nAssistant:",
                    "parameters": {"max_new_tokens": 300, "temperature": 0.8}
                }
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").split("Assistant:")[-1].strip()
                return result.get("generated_text", "").strip()
            except Exception as e:
                raise Exception(f"Hugging Face API error: {str(e)}")
        
        # Together AI (FREE tier available)
        elif provider == "together":
            if not TOGETHER_API_KEY:
                raise ValueError("TOGETHER_API_KEY not set")
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {TOGETHER_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": os.getenv("TOGETHER_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1"),
                    "messages": [
                        {"role": "system", "content": get_dm_prompt()},
                        {"role": "user", "content": context}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 300
                }
                response = requests.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            except Exception as e:
                raise Exception(f"Together AI API error: {str(e)}")
        
        # Ollama (LOCAL - Completely FREE, no API key needed!)
        elif provider == "ollama":
            try:
                import requests
                model = os.getenv("OLLAMA_MODEL", "llama3.2")
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": get_dm_prompt()},
                        {"role": "user", "content": context}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.8, "num_predict": 300}
                }
                response = requests.post(
                    f"{OLLAMA_BASE_URL}/api/chat",
                    json=payload,
                    timeout=60
                )
                result = response.json()
                return result["message"]["content"].strip()
            except Exception as e:
                raise Exception(f"Ollama error: {str(e)}. Make sure Ollama is running: ollama serve")
        
        # Fallback if provider not recognized
        else:
            raise ValueError(f"Unknown AI provider: {provider}. Use: openai, groq, ollama, huggingface, or together")
    
    except Exception as e:
        # Fallback narrative if AI fails
        return f"You {player_action.lower()}. The world responds to your actions, though the details are unclear. (Error: {str(e)})"


# ==================== ACTION PROCESSOR ====================

def process_action(action: str, game_state: GameState) -> Dict[str, Any]:
    """Process player action and apply rules"""
    action_lower = action.lower()
    events = []
    narrative = ""
    
    # Check for item usage and remove from inventory
    used_items = []
    for item in game_state.inventory[:]:  # Copy list to avoid modification during iteration
        item_lower = item.lower()
        # Check if action mentions using, giving, offering, presenting, or consuming the item
        if any(word in action_lower for word in ["use", "give", "offer", "present", "consume", "drink", "eat", "throw", "drop", "hand", "show"]):
            if item_lower in action_lower:
                used_items.append(item)
                game_state.inventory.remove(item)
                game_state.add_note("Item Used", f"Used {item} during an action", "Item")
                events.append({
                    "type": "item_used",
                    "description": f"Used: {item}",
                    "item": item
                })
    
    # Combat actions
    if any(word in action_lower for word in ["attack", "strike", "hit", "fight", "combat"]):
        if game_state.monsters:
            monster = game_state.monsters[0]
            attack_result = RuleEngine.attack_roll(
                game_state.character.level,
                game_state.character.get_modifier("strength"),
                monster.get("ac", 12)
            )
            
            if attack_result["hit"]:
                damage_result = RuleEngine.damage_roll(
                    1, 6, game_state.character.get_modifier("strength"),
                    attack_result["critical"]
                )
                monster["hp"] = RuleEngine.calculate_hp(
                    monster.get("max_hp", 20),
                    monster["hp"],
                    damage_result["total"]
                )
                
                events.append({
                    "type": "combat",
                    "description": f"Attack roll: {attack_result['roll']} + {attack_result['modifier']} = {attack_result['total']} {'(CRITICAL!)' if attack_result['critical'] else ''}",
                    "damage": damage_result["total"],
                    "monster_hp": monster["hp"]
                })
                
                if monster["hp"] <= 0:
                    xp_gain = RuleEngine.calculate_xp(monster.get("cr", 1))
                    game_state.character.add_xp(xp_gain)
                    monster_name = monster.get("name", "Monster")
                    game_state.add_note("Victory", f"Defeated {monster_name} and gained {xp_gain} XP", "Combat")
                    game_state.monsters.remove(monster)
                    events.append({
                        "type": "victory",
                        "description": f"Monster defeated! Gained {xp_gain} XP",
                        "xp": xp_gain
                    })
            else:
                events.append({
                    "type": "combat",
                    "description": f"Attack missed! Roll: {attack_result['roll']} + {attack_result['modifier']} = {attack_result['total']} (needed {monster.get('ac', 12)})"
                })
        else:
            events.append({
                "type": "info",
                "description": "No enemies to attack"
            })
    
    # Skill checks
    elif any(word in action_lower for word in ["climb", "jump", "acrobatics"]):
        check = RuleEngine.skill_check(
            game_state.character.get_modifier("dexterity"),
            game_state.character.level // 4,
            12
        )
        events.append({
            "type": "skill_check",
            "description": f"Dexterity check: {check['roll']} + {check['modifier']} = {check['total']} {'(Success!)' if check['success'] else '(Failed)'}",
            "success": check["success"]
        })
    
    elif any(word in action_lower for word in ["search", "investigate", "perception"]):
        check = RuleEngine.skill_check(
            game_state.character.get_modifier("wisdom"),
            game_state.character.level // 4,
            10
        )
        events.append({
            "type": "skill_check",
            "description": f"Wisdom check: {check['roll']} + {check['modifier']} = {check['total']} {'(Success!)' if check['success'] else '(Failed)'}",
            "success": check["success"]
        })
    
    # Movement
    elif any(word in action_lower for word in ["move", "go", "walk", "run", "north", "south", "east", "west"]):
        events.append({
            "type": "movement",
            "description": "You move through the dungeon"
        })
        # Random chance of encountering monster
        if random.random() < 0.3 and not game_state.monsters:
            game_state.monsters.append({
                "name": "Goblin",
                "hp": 15,
                "max_hp": 15,
                "ac": 12,
                "cr": 1
            })
            events.append({
                "type": "encounter",
                "description": "A goblin appears!"
            })
    
    # Rest/heal
    elif any(word in action_lower for word in ["rest", "heal", "sleep"]):
        heal_amount = RuleEngine.roll_d6(1) + game_state.character.level
        old_hp = game_state.character.current_hp
        game_state.character.current_hp = min(
            game_state.character.max_hp,
            game_state.character.current_hp + heal_amount
        )
        events.append({
            "type": "heal",
            "description": f"Restored {game_state.character.current_hp - old_hp} HP",
            "heal_amount": game_state.character.current_hp - old_hp
        })
    
    # Pet/Assistant actions
    elif any(word in action_lower for word in ["pet", "companion", "assistant", "summon", "call pet", "tame"]):
        if not game_state.pet:
            # Summon/create a pet
            game_state.pet = Pet()
            pet_note = f"Tamed {game_state.pet.name}, a {game_state.pet.type} with abilities: {', '.join(game_state.pet.abilities)}"
            game_state.add_note("Pet Tamed", pet_note, "Companion")
            events.append({
                "type": "pet_summoned",
                "description": f"A {game_state.pet.type} named {game_state.pet.name} appears and bonds with you!",
                "pet": game_state.pet.to_dict()
            })
        else:
            events.append({
                "type": "pet_interaction",
                "description": f"You interact with {game_state.pet.name}. Bond: {game_state.pet.bond}%"
            })
    
    elif any(word in action_lower for word in ["pet help", "pet scout", "pet track", "pet fetch"]):
        if game_state.pet:
            # Pet uses an ability
            ability = random.choice(game_state.pet.abilities)
            check = RuleEngine.skill_check(
                game_state.pet.level + 2,  # Pet's skill level
                0,
                10
            )
            if check["success"]:
                game_state.pet.bond = min(100, game_state.pet.bond + 5)
                events.append({
                    "type": "pet_ability",
                    "description": f"{game_state.pet.name} uses {ability}! Success! (Bond +5%)",
                    "ability": ability,
                    "success": True
                })
            else:
                events.append({
                    "type": "pet_ability",
                    "description": f"{game_state.pet.name} tries to {ability.lower()} but fails.",
                    "ability": ability,
                    "success": False
                })
        else:
            events.append({
                "type": "info",
                "description": "You don't have a pet companion yet. Try 'summon pet' or 'call companion'."
            })
    
    # Default action
    else:
        events.append({
            "type": "action",
            "description": f"Attempted: {action}"
        })
    
    # Generate narrative from AI
    narrative = generate_narrative(action, events, game_state)
    
    # Update conversation history for context continuity
    game_state.conversation_history.append(f"Player: {action} | Response: {narrative}")
    if len(game_state.conversation_history) > 10:  # Keep last 10 entries
        game_state.conversation_history.pop(0)
    
    # If items were used but not already tracked, check narrative for item usage
    if not used_items:
        narrative_lower = narrative.lower()
        for item in game_state.inventory[:]:
            item_lower = item.lower()
            # Check if narrative mentions the item being used/given/consumed
            if any(word in narrative_lower for word in ["used", "gave", "offered", "presented", "consumed", "handed", "showed"]):
                if item_lower in narrative_lower:
                    # Check if it's actually being used (not just mentioned)
                    item_context = narrative_lower[narrative_lower.find(item_lower):narrative_lower.find(item_lower)+len(item_lower)+50]
                    if any(word in item_context for word in ["use", "give", "offer", "present", "hand", "show", "pull", "hold"]):
                        used_items.append(item)
                        game_state.inventory.remove(item)
                        game_state.add_note("Item Used", f"Used {item} during an action", "Item")
    
    # Extract and track NPCs mentioned in narrative
    # Simple extraction - look for common NPC indicators
    npc_keywords = ["goblin", "orc", "merchant", "guard", "wizard", "dragon", "knight", "villager", "npc", "ally", "companion", "friend"]
    mentioned_npcs = []
    narrative_lower = narrative.lower()
    for keyword in npc_keywords:
        if keyword in narrative_lower and keyword not in [npc.lower() for npc in game_state.current_npcs]:
            # Check if it's a current interaction (not just mentioned)
            if any(word in narrative_lower for word in ["talks", "says", "responds", "replies", "conversation", "speaks", "thanks", "thank", "joins", "allies", "befriends"]):
                mentioned_npcs.append(keyword.capitalize())
                # Check if it's an ally (friendly NPC)
                if any(word in narrative_lower for word in ["joins", "allies", "befriends", "friend", "companion", "helps"]):
                    if keyword.capitalize() not in game_state.allies:
                        game_state.allies.append(keyword.capitalize())
                        game_state.add_note("New Ally", f"Met and befriended {keyword.capitalize()}", "Alliance")
    
    if mentioned_npcs:
        game_state.current_npcs = list(set(game_state.current_npcs + mentioned_npcs))
    
    # Clear NPCs if player moves away or ends interaction
    if any(word in action_lower for word in ["leave", "go", "move", "walk", "run", "flee", "exit"]):
        game_state.current_npcs = []
    
    game_state.turn_count += 1
    game_state.game_history.append({
        "turn": game_state.turn_count,
        "action": action,
        "events": events,
        "narrative": narrative,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "narrative": narrative,
        "events": events,
        "game_state": game_state.to_dict()
    }


# ==================== API ROUTES ====================

@app.get("/")
def root():
    return {"message": "AI Dungeon Master API"}


@app.post("/api/action", response_model=Dict[str, Any])
async def process_player_action(request: ActionRequest):
    """Process a player action"""
    session_id = request.session_id
    
    # Get or create game state
    if session_id not in game_states:
        game_states[session_id] = GameState()
    
    game_state = game_states[session_id]
    
    try:
        result = process_action(request.action, game_state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/game-state/{session_id}", response_model=GameStateResponse)
async def get_game_state(session_id: str):
    """Get current game state"""
    if session_id not in game_states:
        game_states[session_id] = GameState()
    
    state = game_states[session_id]
    return GameStateResponse(**state.to_dict())


@app.post("/api/new-game/{session_id}")
async def new_game(session_id: str):
    """Start a new game"""
    game_states[session_id] = GameState()
    return {"message": "New game started", "game_state": game_states[session_id].to_dict()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

