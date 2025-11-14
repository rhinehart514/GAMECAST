# 🏗️ Architecture Overview

## System Design: Living Game Architecture

This document explains how the NHL Simulation Game achieves "living AI" - gameplay that automatically improves as the prediction model improves.

## Core Concept

```
Traditional Game              Living Game
┌─────────────────┐          ┌──────────────────────────┐
│  Game Code      │          │  Game Client             │
│  with           │          │    ↓ queries             │
│  Hardcoded AI   │          │  Intelligence API        │
│                 │          │    ↓ uses                │
│  ❌ Static      │          │  Puckcast Model v1, v2...│
│  ❌ Manual      │          │                          │
│  ❌ Expensive   │          │  ✅ Dynamic              │
└─────────────────┘          │  ✅ Automatic            │
                             │  ✅ Evolving             │
                             └──────────────────────────┘
```

## System Components

### 1. Puckcast Model (Separate Project)
```
../puckcast/
├── src/nhl_prediction/
│   ├── model.py           ← The ML model
│   ├── pipeline.py        ← Feature engineering
│   ├── features.py        ← Feature definitions
│   └── data_ingest.py     ← Data loading
└── data/
    └── *.csv              ← Training data
```

**Status:** Already exists, don't modify
**Role:** Provides predictions
**Owner:** Model developer

### 2. Intelligence Service (This Project)
```
nhl-simulation-game/intelligence-service/
├── src/
│   ├── api/
│   │   └── endpoints.py       ← FastAPI endpoints
│   ├── model_client/
│   │   └── puckcast_client.py ← Wrapper around Puckcast
│   └── main.py                ← Server entry point
└── requirements.txt
```

**Status:** Just created!
**Role:** Exposes model as REST API
**Technology:** FastAPI, Python 3.9+

### 3. Game Engine (To Build)
```
nhl-simulation-game/game-engine/
├── src/
│   ├── simulator/
│   │   ├── game.py        ← Core game simulation
│   │   └── play_by_play.py ← Event generation
│   ├── entities/
│   │   ├── team.py        ← Team objects
│   │   └── player.py      ← Player objects
│   └── state/
│       └── game_state.py  ← Game state management
└── pyproject.toml
```

**Status:** To be built (Week 2)
**Role:** Simulates games using AI
**Technology:** Python 3.9+

### 4. Game Client (To Build)
```
nhl-simulation-game/game-client/
├── cli/
│   └── play.py            ← Command-line interface
└── web/
    ├── pages/             ← Next.js pages
    ├── components/        ← React components
    └── lib/               ← API client
```

**Status:** CLI test client exists, web UI to build (Week 3)
**Role:** User interface
**Technology:** Python (CLI), Next.js + TypeScript (web)

## Data Flow

### Example: Simulating a Game

```
1. User Action
   ┌─────────────────┐
   │ User clicks     │
   │ "Simulate Game" │
   └────────┬────────┘
            │
            ▼
2. Game Client Request
   ┌──────────────────────┐
   │ POST /simulate-game  │
   │ {                    │
   │   home: "BOS",       │
   │   away: "TOR"        │
   │ }                    │
   └──────────┬───────────┘
              │
              ▼
3. Game Engine Queries AI
   ┌────────────────────────────┐
   │ GameSimulator               │
   │   while not game_over:     │
   │     decision = ai.predict()│
   │     execute(decision)      │
   └──────────┬─────────────────┘
              │
              ▼
4. Intelligence Service Call
   ┌────────────────────────────┐
   │ POST /predict-game         │
   │ {                          │
   │   period: 2,               │
   │   time: 10.5,              │
   │   score_home: 2,           │
   │   score_away: 1            │
   │ }                          │
   └──────────┬─────────────────┘
              │
              ▼
5. Model Prediction
   ┌────────────────────────────┐
   │ PuckcastClient             │
   │   features = extract()     │
   │   pred = model.predict()   │
   │   return prediction        │
   └──────────┬─────────────────┘
              │
              ▼
6. Response
   ┌────────────────────────────┐
   │ {                          │
   │   home_win_prob: 0.63,     │
   │   away_win_prob: 0.37,     │
   │   confidence: 0.82         │
   │ }                          │
   └──────────┬─────────────────┘
              │
              ▼
7. Game Engine Decision
   ┌────────────────────────────┐
   │ Based on 63% probability:  │
   │   - More shots for BOS     │
   │   - Higher goal chance     │
   │   - Smarter AI decisions   │
   └──────────┬─────────────────┘
              │
              ▼
8. User Sees Result
   ┌────────────────────────────┐
   │ Period 2: BOS 3 - TOR 1    │
   │ "Boston scores! AI saw     │
   │  high-quality shot opp"    │
   └────────────────────────────┘
```

## API Contracts

### Intelligence Service → Puckcast Model

```python
# Intelligence service calls Puckcast
from nhl_prediction.model import predict_probabilities

result = model.predict_proba(features)
# Returns: [[away_prob, home_prob]]
```

**Contract:**
- Input: Feature array (141 features)
- Output: Probability array [away, home]
- Model version tracked separately

### Game Engine → Intelligence Service

```python
# Game engine calls intelligence API
import httpx

response = httpx.post("http://localhost:8000/predict-game", json={
    "home_team_id": 6,
    "away_team_id": 10,
    "period": 2,
    "time_remaining": 10.5,
    "score_home": 2,
    "score_away": 1
})

prediction = response.json()
# Returns: {home_win_prob, away_win_prob, ...}
```

**Contract:**
- Input: GameStateRequest (Pydantic model)
- Output: PredictionResponse (Pydantic model)
- HTTP/REST over port 8000

### Game Client → Game Engine

```typescript
// Web client calls game engine
const response = await fetch('/api/simulate', {
  method: 'POST',
  body: JSON.stringify({
    homeTeam: 'BOS',
    awayTeam: 'TOR',
    options: {...}
  })
});

const game = await response.json();
```

**Contract:**
- Input: Game parameters
- Output: Full game result with events
- Websocket for real-time updates (future)

## Deployment Architecture

### Development (Local)

```
Your Machine
├── Terminal 1: intelligence-service (port 8000)
├── Terminal 2: game-engine (if CLI)
└── Browser: game client (if web)
```

### Production (Cloud)

```
┌─────────────────────────────────────────┐
│  User's Browser                         │
│  (game-client/web)                      │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Vercel / Netlify                       │
│  (Static hosting for web client)        │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Game Engine API                        │
│  (Railway / Render / Fly.io)            │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Intelligence Service                   │
│  (Railway / Render / Fly.io)            │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Puckcast Model (loaded in memory)      │
│  + Redis cache for predictions          │
└─────────────────────────────────────────┘
```

## Key Design Decisions

### 1. **Separate Projects**
**Decision:** Keep game and model in separate directories

**Why:**
- Model is research project, game is product
- Different development cycles
- Can update model without touching game
- Clear ownership boundaries

**Trade-off:** Need integration layer (intelligence service)

### 2. **REST API (not library import)**
**Decision:** Game calls model via HTTP, not direct import

**Why:**
- Loose coupling - can swap model easily
- Can version models independently
- Can scale services separately
- Can A/B test model versions
- Language agnostic (could write game in any language)

**Trade-off:** Slight latency (~50ms vs ~1ms)

### 3. **Stateless Intelligence Service**
**Decision:** Service doesn't store game state

**Why:**
- Simpler to scale (no state to manage)
- Game engine owns game state
- Can restart service without losing games
- Multiple games can use same service

**Trade-off:** Game must send full context each call

### 4. **Pydantic Models**
**Decision:** Use Pydantic for API contracts

**Why:**
- Type safety
- Automatic validation
- Self-documenting (OpenAPI/Swagger)
- Easy to version

**Trade-off:** None really, this is best practice

## Model Evolution Flow

### How Model Improvements Flow to Game

```
Week 1: Game v1.0 + Model v1.0
┌────────────────────────────────┐
│ Game asks: "Should pull goalie?"
│ Model (v1.0): Uses basic logic
│ Result: OK decisions
└────────────────────────────────┘

Week 4: Model developer improves model
┌────────────────────────────────┐
│ 1. cd ../puckcast
│ 2. Add fatigue features
│ 3. Retrain model
│ 4. Save as model v2.0
└────────────────────────────────┘

Week 4: Deploy new model
┌────────────────────────────────┐
│ 1. Restart intelligence service
│ 2. Loads model v2.0 automatically
│ 3. NO game code changes!
└────────────────────────────────┘

Week 4: Game v1.0 + Model v2.0
┌────────────────────────────────┐
│ Game asks: "Should pull goalie?"
│ Model (v2.0): Considers fatigue now!
│ Result: BETTER decisions
│ 🎉 Game improved automatically!
└────────────────────────────────┘
```

## Technology Stack

### Intelligence Service
- **Language:** Python 3.9+
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Validation:** Pydantic
- **ML:** scikit-learn (from Puckcast)

### Game Engine
- **Language:** Python 3.9+
- **HTTP Client:** httpx
- **Testing:** pytest
- **Package:** setuptools

### Game Client (CLI)
- **Language:** Python 3.9+
- **HTTP Client:** httpx
- **Rich terminal:** Rich library (future)

### Game Client (Web)
- **Framework:** Next.js 14
- **Language:** TypeScript
- **UI:** React + Tailwind CSS
- **API Client:** fetch / SWR

## Performance Considerations

### Latency Budget

```
User clicks simulate
  ↓ 0ms
Game engine processes
  ↓ 10ms
HTTP call to intelligence
  ↓ 50ms (local) / 200ms (cloud)
Model inference
  ↓ 10ms
Response back
  ↓ 50ms (local) / 200ms (cloud)
Game engine continues
  ↓ 10ms
Total: ~130ms (local) / ~490ms (cloud)
```

**Goal:** <500ms for each game decision
**Status:** Well within budget ✅

### Caching Strategy

```python
# Cache predictions for identical game states
@lru_cache(maxsize=1000)
def predict_game_outcome(state_hash):
    return model.predict(state)
```

**Benefit:** Repeat scenarios instant
**Trade-off:** More memory usage

### Batch Predictions (Future)

```python
# For season simulation: batch predictions
predictions = model.predict_batch([
    game1_features,
    game2_features,
    # ... 100 games
])
# Much faster than 100 individual calls
```

## Security Considerations

### Development
- ✅ Service runs on localhost only
- ✅ No authentication needed

### Production
- 🎯 Add API key authentication
- 🎯 Rate limiting (100 req/min per user)
- 🎯 HTTPS only
- 🎯 Input validation (Pydantic does this)
- 🎯 No sensitive data in predictions

## Next Steps

1. **Complete Intelligence Service** ✅
   - FastAPI endpoints ✅
   - Puckcast client ✅
   - Testing done

2. **Build Game Engine** (Week 2)
   - Game simulation logic
   - Query intelligence API
   - Generate play-by-play

3. **Build Web UI** (Week 3)
   - Next.js app
   - Game interface
   - Real-time updates

4. **Deploy** (Week 4)
   - Host intelligence service
   - Host game engine
   - Deploy web app

---

**See Also:**
- [GETTING_STARTED.md](../GETTING_STARTED.md) - Setup guide
- [API_REFERENCE.md](API_REFERENCE.md) - API documentation
- [GAME_DESIGN.md](GAME_DESIGN.md) - Gameplay mechanics

