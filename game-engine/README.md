# NHL Game Engine

**AI-Powered Hockey Simulation with Living Intelligence**

---

## Overview

The game engine simulates complete NHL hockey games with realistic events, stats tracking, and **AI-driven decision making** via the Intelligence Service API.

### Key Features

✅ **Full Game Simulation**
- 3 periods (20 minutes each)
- Overtime (3v3)
- Shootouts
- Real-time event generation

✅ **Realistic Events**
- Goals, shots, saves
- Penalties and power plays
- Hits, blocked shots
- Faceoffs
- Goalie pulls

✅ **AI Decision Making**
- Queries Intelligence Service for strategic decisions
- Smart goalie pull timing
- Adapts to game situations
- **Improves automatically as ML model improves!**

✅ **Comprehensive Stats**
- Shots, shot attempts
- Corsi/Fenwick
- Expected goals (xG)
- Faceoffs, hits, blocks
- Power play tracking
- Penalty statistics

---

## Architecture

```
Game Engine (simulator.py)
    ↓ Game Events
    ↓ Strategic Decision Needed?
    ↓ HTTP Request
Intelligence Service API
    ↓ Query ML Model
Puckcast Prediction Model
    ↓ AI Recommendation
Intelligence Service
    ↓ HTTP Response
Game Engine
    ↓ Execute Decision
Continue Simulation
```

**The "Living Game" Advantage:**
When the Puckcast model creator improves the ML model, your game AI gets smarter automatically—no code changes needed!

---

## Files

### `game_state.py`
Complete game state management:
- `GameState` - Full game tracking
- `TeamState` - Team stats and status
- `GameEvent` - Event logging
- `GamePeriod`, `EventType`, `StrengthSituation` - Enums

### `simulator.py`
Main simulation engine:
- `NHLSimulator` - Core simulator class
- Event generation logic
- AI decision integration
- Game flow management

### `demo.py`
Interactive demo script:
- Pre-configured matchups
- Custom game setup
- Multiple game simulation
- Results summary

---

## Quick Start

### 1. Start Intelligence Service

```bash
# Terminal 1
cd intelligence-service/src
python main.py
```

Wait for: `INFO: Application startup complete`

### 2. Run Simulation

```bash
# Terminal 2
cd game-engine
python demo.py
```

Follow the interactive prompts!

---

## Usage Examples

### Basic Simulation

```python
from simulator import NHLSimulator

# Initialize simulator
sim = NHLSimulator(api_url="http://localhost:8000")

# Simulate game
game = sim.simulate_game(
    home_team_code="TOR",
    home_team_name="Toronto Maple Leafs",
    away_team_code="MTL",
    away_team_name="Montreal Canadiens"
)

# Get results
winner = game.get_winner()
print(f"Winner: {winner.name}")
print(f"Final Score: {game.away_team.score} - {game.home_team.score}")
```

### With Event Callback

```python
def on_event(event):
    """Handle game events."""
    if event.event_type == EventType.GOAL:
        print(f"GOAL! {event.team} scores!")

sim = NHLSimulator(
    api_url="http://localhost:8000",
    event_callback=on_event
)

game = sim.simulate_game("TOR", "Toronto Maple Leafs", "MTL", "Montreal Canadiens")
```

### Silent Mode (No Console Output)

```python
sim = NHLSimulator(verbose=False)
game = sim.simulate_game("BOS", "Boston Bruins", "NYR", "New York Rangers")
```

---

## Game State API

### Access Game Information

```python
# Current score
home_score = game.home_team.score
away_score = game.away_team.score

# Game time
period = game.period  # GamePeriod enum
time_left = game.time_remaining  # seconds

# Stats
shots = game.home_team.shots
xg = game.home_team.expected_goals
pp_pct = game.home_team.power_play_goals / max(game.home_team.power_play_opportunities, 1)

# Events
for event in game.events:
    print(f"{event.period.value}P {event.time_remaining}s: {event.description}")

# Export to dict (for API calls)
game_dict = game.to_dict()
```

---

## AI Decision Points

The simulator queries the Intelligence Service API for strategic decisions:

### Goalie Pull Decision
- **When:** Trailing in late game (Period 3 or OT)
- **API Call:** `POST /recommend-decision`
- **Factors:**
  - Score differential
  - Time remaining
  - Game situation
  - ML model confidence
- **Fallback:** Simple rule-based logic if API unavailable

**Example API Request:**
```json
{
  "game_state": {
    "period": 3,
    "time_remaining": 90,
    "home_team": {"score": 2, ...},
    "away_team": {"score": 3, ...}
  },
  "decision_type": "pull_goalie",
  "context": {
    "score_diff": -1,
    "time_remaining": 90,
    "period": 3
  }
}
```

**Example API Response:**
```json
{
  "recommendation": "pull_goalie",
  "confidence": 0.75,
  "reasoning": "Down 1 goal with 1.5 min left",
  "model_version": "1.0.0"
}
```

---

## Event Types

- **GOAL** - Goal scored
- **SHOT** - Shot on goal (save)
- **BLOCKED_SHOT** - Shot blocked by defender
- **PENALTY** - Penalty called
- **FACEOFF** - Faceoff
- **HIT** - Body check
- **GOALIE_PULL** - Goalie pulled for extra attacker
- **PERIOD_START** - Period begins
- **PERIOD_END** - Period ends
- **GAME_END** - Game over

---

## Strength Situations

- **5v5** - Even strength
- **5v4** - Power play (major)
- **5v3** - Power play (minor)
- **4v5** - Shorthanded (major)
- **3v5** - Shorthanded (minor)
- **4v4** - Four-on-four
- **3v3** - Three-on-three (OT)

---

## Sample Output

```
======================================================================
SIMULATING: Montreal Canadiens @ Toronto Maple Leafs
======================================================================

--- Period 1 ---

[1P 18:45] PENALTY: Toronto Maple Leafs - Slashing (2 min)
[1P 17:20] ⚡ GOAL! Montreal Canadiens! (1-0)
[1P 15:30] Save by Toronto Maple Leafs
[1P 12:40] Big hit by Toronto Maple Leafs!
[1P 08:15] ⚡ GOAL! Toronto Maple Leafs! (1-1)

--- Period 2 ---

[2P 14:22] ⚡ GOAL! Toronto Maple Leafs! (1-2)
[2P 09:35] PENALTY: Montreal Canadiens - Hooking (2 min)
[2P 08:10] ⚡ GOAL! Toronto Maple Leafs! (Power Play) (1-3)

--- Period 3 ---

[3P 05:45] ⚡ GOAL! Montreal Canadiens! (2-3)
[3P 01:30] 🎯 AI DECISION: Montreal Canadiens pulls goalie!
[3P 00:55] ⚡ GOAL! Montreal Canadiens! (3-3)

--- Overtime ---

[4P 03:12] ⚡ GOAL! Toronto Maple Leafs! (3-4)

======================================================================
FINAL SCORE
======================================================================
Montreal Canadiens: 3
Toronto Maple Leafs: 4

Winner: Toronto Maple Leafs
======================================================================

GAME STATS
======================================================================
Stat                       MTL        TOR
----------------------------------------------------------------------
Shots                       28         32
Shot Attempts               45         48
Hits                        18         22
Blocked Shots               12         15
Faceoff Wins                31         29
Penalties                    2          1
PP Goals/Opps              0/1        1/2
Expected Goals            3.45       4.20
======================================================================
```

---

## Future Enhancements

Planned for Week 3-4:

- [ ] Line change decisions
- [ ] Offensive/defensive strategy selection
- [ ] Timeout management
- [ ] Player fatigue modeling
- [ ] Injury simulation
- [ ] Hot goalie streaks
- [ ] Home ice advantage modeling
- [ ] Real-time odds calculation
- [ ] Live game visualization

---

## Troubleshooting

### "Connection refused" error
Intelligence Service isn't running. Start it:
```bash
cd intelligence-service/src
python main.py
```

### Simulation feels unrealistic
Adjust probabilities in `simulator.py`:
- Shot rates: `event_weights['shot']`
- Goal probability: `base_goal_prob`
- Penalty rates: `event_weights['penalty']`

### AI decisions not triggering
- Check API connection
- Verify fallback logic in `_should_pull_goalie()`
- Enable verbose mode: `NHLSimulator(verbose=True)`

---

## Contributing

Want to add new AI decision points?

1. Add decision type to Intelligence Service API
2. Create `_check_<decision>()` method in simulator
3. Call from `_check_ai_decisions()`
4. Add fallback logic for offline mode

Example:
```python
def _check_line_change(self, game: GameState):
    """Query AI for line change decision."""
    response = self.client.post(
        f"{self.api_url}/recommend-decision",
        json={
            "game_state": game.to_dict(),
            "decision_type": "line_change"
        }
    )
    # Process response...
```

---

**Built with ❤️ for the love of hockey and AI**

