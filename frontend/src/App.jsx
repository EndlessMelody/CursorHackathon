import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './App.css'

// Dice Roll Animation Component
function DiceRollAnimation({ event }) {
  const [rolling, setRolling] = useState(true)
  const [finalRoll, setFinalRoll] = useState(null)
  const [diceValues, setDiceValues] = useState([1, 1])
  const rollIntervalRef = useRef(null)

  useEffect(() => {
    // Extract roll value from event description
    const rollMatch = event.description.match(/(\d+)\s*\+/);
    const roll = rollMatch ? parseInt(rollMatch[1]) : null;
    
    if (roll) {
      setFinalRoll(roll);
      // Animate dice rolling
      rollIntervalRef.current = setInterval(() => {
        setDiceValues([
          Math.floor(Math.random() * 20) + 1,
          Math.floor(Math.random() * 20) + 1
        ]);
      }, 100);

      // Stop after 1.5 seconds
      setTimeout(() => {
        setRolling(false);
        if (rollIntervalRef.current) {
          clearInterval(rollIntervalRef.current);
        }
        setDiceValues([roll, roll]);
      }, 1500);
    } else {
      setRolling(false);
    }

    return () => {
      if (rollIntervalRef.current) {
        clearInterval(rollIntervalRef.current);
      }
    };
  }, [event]);

  if (!finalRoll) {
    return (
      <div className="event-item" style={{ borderLeftColor: '#4ecdc4' }}>
        <span className="event-icon">🎲</span>
        <span className="event-description">{event.description}</span>
      </div>
    );
  }

  return (
    <div className="dice-roll-container">
      <div className="event-item" style={{ borderLeftColor: '#4ecdc4' }}>
        <span className="event-icon">🎲</span>
        <div className="dice-animation">
          <div className="dice-wrapper">
            {[0, 1].map((i) => (
              <div key={i} className={`dice ${rolling ? 'rolling' : ''}`}>
                {rolling ? diceValues[i] : finalRoll}
              </div>
            ))}
          </div>
          <span className="event-description">{event.description}</span>
        </div>
      </div>
    </div>
  );
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function App() {
  const [gameState, setGameState] = useState(null)
  const [action, setAction] = useState('')
  const [loading, setLoading] = useState(false)
  const [narrative, setNarrative] = useState('')
  const [events, setEvents] = useState([])
  const [sessionId] = useState(() => `session_${Date.now()}`)
  const narrativeEndRef = useRef(null)
  const actionInputRef = useRef(null)

  useEffect(() => {
    initializeGame()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [narrative, events])

  const scrollToBottom = () => {
    narrativeEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const initializeGame = async () => {
    try {
      const response = await axios.post(`${API_BASE}/api/new-game/${sessionId}`)
      await loadGameState()
      // Use the random starting narrative from backend
      const startingNarrative = response.data.starting_narrative || 'Welcome, brave adventurer! Your journey begins...'
      setNarrative(startingNarrative)
    } catch (error) {
      console.error('Failed to initialize game:', error)
    }
  }

  const loadGameState = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/game-state/${sessionId}`)
      setGameState(response.data)
    } catch (error) {
      console.error('Failed to load game state:', error)
    }
  }

  const handleAction = async (e) => {
    e.preventDefault()
    if (!action.trim() || loading) return

    const actionText = action.trim()
    setAction('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE}/api/action`, {
        action: actionText,
        session_id: sessionId
      })

      setNarrative(response.data.narrative)
      setEvents(response.data.events || [])
      setGameState(response.data.game_state)
    } catch (error) {
      console.error('Action failed:', error)
      setNarrative('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
      actionInputRef.current?.focus()
    }
  }

  const getEventIcon = (type) => {
    const icons = {
      combat: '⚔️',
      skill_check: '🎲',
      movement: '🚶',
      heal: '💚',
      encounter: '👹',
      victory: '🏆',
      action: '✨',
      info: 'ℹ️',
      pet_summoned: '🐾',
      pet_interaction: '🐕',
      pet_ability: '🌟',
      dice_roll: '🎲',
      item_used: '📦'
    }
    return icons[type] || '✨'
  }

  const getEventColor = (type) => {
    const colors = {
      combat: '#ff6b6b',
      skill_check: '#4ecdc4',
      movement: '#95e1d3',
      heal: '#51cf66',
      encounter: '#ff8787',
      victory: '#ffd43b',
      action: '#74c0fc',
      info: '#adb5bd'
    }
    return colors[type] || '#adb5bd'
  }

  if (!gameState) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Initializing your adventure...</p>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🗡️ AI Dungeon Master</h1>
        <div className="character-stats">
          <div className="stat">
            <span className="stat-label">Level</span>
            <span className="stat-value">{gameState.character.level}</span>
          </div>
          <div className="stat">
            <span className="stat-label">HP</span>
            <span className="stat-value">
              {gameState.character.current_hp}/{gameState.character.max_hp}
            </span>
            <div className="hp-bar">
              <div 
                className="hp-fill" 
                style={{ 
                  width: `${(gameState.character.current_hp / gameState.character.max_hp) * 100}%` 
                }}
              />
            </div>
          </div>
          <div className="stat">
            <span className="stat-label">XP</span>
            <span className="stat-value">{gameState.character.xp}</span>
          </div>
          <div className="stat">
            <span className="stat-label">AC</span>
            <span className="stat-value">{gameState.character.ac}</span>
          </div>
        </div>
      </header>

      <div className="game-container">
        <div className="narrative-panel">
          <div className="narrative-content">
            <div className="narrative-text">
              {narrative || 'The adventure begins...'}
            </div>
            {events.length > 0 && (
              <div className="events-list">
                {events.map((event, idx) => {
                  // Show dice animation for combat and skill checks
                  if (event.type === 'skill_check' || event.type === 'combat') {
                    return <DiceRollAnimation key={idx} event={event} />
                  }
                  return (
                    <div 
                      key={idx} 
                      className="event-item"
                      style={{ borderLeftColor: getEventColor(event.type) }}
                    >
                      <span className="event-icon">{getEventIcon(event.type)}</span>
                      <span className="event-description">{event.description}</span>
                    </div>
                  )
                })}
              </div>
            )}
            <div ref={narrativeEndRef} />
          </div>
        </div>

        <div className="sidebar">
          <div className="sidebar-section">
            <h3>📍 Location</h3>
            <p>{gameState.location}</p>
          </div>

          {gameState.monsters.length > 0 && (
            <div className="sidebar-section">
              <h3>👹 Enemies</h3>
              {gameState.monsters.map((monster, idx) => (
                <div key={idx} className="monster-info">
                  <div className="monster-name">{monster.name}</div>
                  <div className="monster-hp">
                    HP: {monster.hp}/{monster.max_hp}
                    <div className="hp-bar small">
                      <div 
                        className="hp-fill" 
                        style={{ 
                          width: `${(monster.hp / monster.max_hp) * 100}%`,
                          backgroundColor: '#ff6b6b'
                        }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {gameState.pet && (
            <div className="sidebar-section">
              <h3>🐾 Companion</h3>
              <div className="pet-info">
                <div className="pet-name">{gameState.pet.name}</div>
                <div className="pet-type">{gameState.pet.type}</div>
                <div className="pet-hp">
                  HP: {gameState.pet.current_hp}/{gameState.pet.max_hp}
                  <div className="hp-bar small">
                    <div 
                      className="hp-fill" 
                      style={{ 
                        width: `${(gameState.pet.current_hp / gameState.pet.max_hp) * 100}%`,
                        backgroundColor: '#9b59b6'
                      }}
                    />
                  </div>
                </div>
                <div className="pet-bond">
                  Bond: {gameState.pet.bond}%
                  <div className="hp-bar small">
                    <div 
                      className="hp-fill" 
                      style={{ 
                        width: `${gameState.pet.bond}%`,
                        backgroundColor: '#e74c3c'
                      }}
                    />
                  </div>
                </div>
                <div className="pet-abilities">
                  <strong>Abilities:</strong>
                  <ul className="abilities-list">
                    {gameState.pet.abilities.map((ability, idx) => (
                      <li key={idx}>{ability}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          <div className="sidebar-section">
            <h3>🎒 Inventory</h3>
            {gameState.inventory.length > 0 ? (
              <ul className="inventory-list">
                {gameState.inventory.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="empty">Empty</p>
            )}
          </div>

          {gameState.allies && gameState.allies.length > 0 && (
            <div className="sidebar-section">
              <h3>🤝 Allies</h3>
              <ul className="allies-list">
                {gameState.allies.map((ally, idx) => (
                  <li key={idx}>{ally}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="sidebar-section">
            <h3>📝 Journal</h3>
            {gameState.notes && gameState.notes.length > 0 ? (
              <div className="notes-list">
                {gameState.notes.slice().reverse().slice(0, 10).map((note, idx) => (
                  <div key={idx} className="note-item">
                    <div className="note-header">
                      <span className="note-category">{note.category}</span>
                      <span className="note-title">{note.title}</span>
                    </div>
                    <div className="note-description">{note.description}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="empty">No notes yet</p>
            )}
          </div>

          <div className="sidebar-section">
            <h3>📊 Abilities</h3>
            <div className="abilities-grid">
              <div className="ability">
                <span>STR</span>
                <span>{gameState.character.strength}</span>
              </div>
              <div className="ability">
                <span>DEX</span>
                <span>{gameState.character.dexterity}</span>
              </div>
              <div className="ability">
                <span>CON</span>
                <span>{gameState.character.constitution}</span>
              </div>
              <div className="ability">
                <span>INT</span>
                <span>{gameState.character.intelligence}</span>
              </div>
              <div className="ability">
                <span>WIS</span>
                <span>{gameState.character.wisdom}</span>
              </div>
              <div className="ability">
                <span>CHA</span>
                <span>{gameState.character.charisma}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="action-bar">
        <form onSubmit={handleAction} className="action-form">
          <input
            ref={actionInputRef}
            type="text"
            value={action}
            onChange={(e) => setAction(e.target.value)}
            placeholder="What do you do? (e.g., 'attack the goblin', 'search the room', 'move north')"
            disabled={loading}
            className="action-input"
            autoFocus
          />
          <button 
            type="submit" 
            disabled={loading || !action.trim()}
            className="action-button"
          >
            {loading ? '...' : 'Act'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App

