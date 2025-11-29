# Dungeon Master AI System Prompt

This is the system prompt used by the AI to generate action-oriented, consequence-driven narrative responses in the game.

## Current Implementation

The system prompt is defined in `backend/app.py` in the `get_dm_prompt()` function. It's designed to:

1. **Treat player input as actions** - Every input is evaluated as an action with consequences
2. **Always provide results** - Every action triggers discoveries, obstacles, NPC interactions, or environmental changes
3. **Include actionable options** - Each response ends with 2-3 specific next actions the player can take
4. **Integrate game events** - Dice rolls, combat results, and skill checks are naturally woven into the narrative

## Key Features

- **Action-Oriented**: Player inputs are treated as actions, not story prompts
- **Consequence-Driven**: Every action must have at least one concrete outcome
- **Interactive**: Always provides 2-3 actionable next steps
- **Event-Integrated**: Game mechanics (dice, combat) are naturally incorporated

## Example Response Format

Good response:
> "You search along the cliff edge and discover a narrow path hidden behind overgrown shrubs. A faint draft and the sound of dripping water suggest a cave ahead. You could approach the path carefully, inspect the shrubs for traps, or call out to check for echoes or creatures inside."

Bad response (too passive):
> "You are in a dark forest. The trees are tall and mysterious."

## Customization

To modify the AI's behavior, edit the `get_dm_prompt()` function in `backend/app.py`. You can:
- Change the tone (serious, humorous, dark, etc.)
- Adjust response length and structure
- Modify the number of actionable options provided
- Add specific instructions for certain scenarios

## Note

This prompt is sent to the AI provider (OpenAI, Groq, etc.) along with rich game context including:
- Player action
- Game events (dice rolls, combat results)
- Current game state (HP, level, inventory, location, enemies)

The actual game mechanics (dice rolls, combat calculations, etc.) are handled by the code-based rule engine, not the AI. The AI's role is to provide engaging narrative that responds to actions and guides the player forward.

