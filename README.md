# Castle War Game

## Overview
Castle War Game is a turn-based strategy game where players manage resources, build armies, and battle to destroy their opponent's castle. The game combines resource management, strategic decision-making, and a unique card system to create an engaging gameplay experience.

## Features

### Core Gameplay
- **Resource Management**: Allocate your population between soldiers (for attacking) and farmers (for healing and boosting damage)
- **Turn-Based Combat**: Strategic gameplay with alternating turns
- **Growing Resources**: Population increases each round, allowing for evolving strategies
- **Multiple Action Types**: Attack, heal, boost damage, or play special cards

### Card System
- **Battle Chest**: 10% chance each turn to receive a random card
- **Endangered Mode**: Automatically receive a card when health drops below 10
- **Card Rarities**: Common, Rare, Epic, and Legendary cards with varying abilities
- **Special Effects**: Counter Shield, Rebirth, Trap Card, Lucky Charm, and more

### Game Modes
- **Single-Player**: Battle against AI opponent
- **Two-Player**: Local multiplayer on the same computer

### Statistics & Analytics
- **Gameplay Tracking**: Records detailed statistics for every game
- **Visualization Dashboard**: Analyze your gameplay with 11 different types of charts and graphs
- **Performance Metrics**: Track win rates, strategy effectiveness, and gameplay patterns

## Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Setup
1. Clone or download the repository
2. Install required dependencies:
   ```
   pip install pygame pandas numpy matplotlib seaborn
   ```
3. Run the game:
   ```
   python main.py
   ```

## Files and Structure

### Core Game Files
- **main.py**: Entry point and main menu system
- **castle_game.py**: Main game mechanics and logic
- **card_system.py**: Card management and effects
- **game_stats.py**: Statistics tracking system
- **config.py**: Game configuration settings

### Visualization System
- **stats_visualizer.py**: Generates statistical visualizations
- **visualization_menu.py**: Interactive dashboard for viewing statistics

## How to Play

1. **Starting the Game**:
   - Launch the game by running `main.py`
   - Choose "Single Player" or "Two Players" from the menu
   - Enter player name(s)

2. **First Round**:
   - In the first round, each player has 1 population unit
   - End your turn to proceed to Round 2

3. **Allocating Population**:
   - Starting from Round 2, use the slider to allocate population between soldiers and farmers
   - Soldiers are used for attacking
   - Farmers can heal hearts or boost damage

4. **Taking Actions**:
   - **Attack**: Use soldiers to damage opponent's castle
   - **Heal**: Use farmers to restore hearts
   - **Boost Damage**: Use farmers to increase attack power
   - **Play Card**: Use special cards for various effects

5. **Using Cards**:
   - Click on a card to select it
   - Click the "PLAY CARD" button to use the selected card
   - Different cards provide different strategic advantages

6. **Winning the Game**:
   - Reduce your opponent's hearts to zero to win
   - The game keeps track of wins and statistics

## Card Types

| Card | Rarity | Effect |
|------|--------|--------|
| Counter Shield | Legendary | Blocks next attack and reflects 50% of damage |
| Rebirth Card | Legendary | Revive with 10 hearts if health reaches 0 |
| Steal Card | Epic | Randomly steal one of opponent's cards |
| Lucky Charm | Epic | Increases chances to get better rarity cards |
| Double Draw | Rare | Draw 2 random cards on next turn |
| Trap Card | Rare | If attacked, enemy loses 10 hearts and has 20% less damage for 2 turns |
| Attack Boost Card | Rare | +30 damage to next attack |
| Heal Card | Common | Heal 10 hearts |
| Population Card | Common | Add 20 population |

## Game Statistics

The game records detailed statistics for every match, including:
- Battle count
- Unit allocation (soldiers vs. farmers)
- Hearts lost
- Game duration
- Action types used
- Win/loss records

Access these statistics through the "Visualization Data" option in the main menu.

## Tips and Strategies

- Balance your resource allocation between soldiers and farmers
- Consider using farmers early to boost damage for stronger attacks later
- Save special cards for critical moments
- Pay attention to your opponent's health - Endangered Mode can give them powerful cards
- In later rounds, your strategy will need to evolve as your population grows

## Future Development

Planned features for future updates:
- Survival mode
- Tutorial system
- New card types
- Online multiplayer

## Credits

Created with Python and Pygame. Visualization system built with Matplotlib, Seaborn, and Pandas.