# 🚀 Getting Started

Welcome to the NHL Simulation Game! This guide will get you up and running in 10 minutes.

## 📁 Project Structure

```
nhl-simulation-game/          ← You are here (the game)
├── intelligence-service/     ← API wrapper around Puckcast model
├── game-engine/              ← Game simulation logic
├── game-client/              ← User interfaces
└── scripts/                  ← Helper scripts

../puckcast/                  ← Separate ML project (don't touch)
└── src/nhl_prediction/       ← The prediction model
```

## ⚡ Quick Start (Windows)

### Step 1: Install Python Dependencies

```bash
cd intelligence-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start the Intelligence Service

```bash
# From intelligence-service/ directory with venv activated
python src/main.py
```

You should see:
```
🏒 NHL Intelligence Service
=============================
Starting server...
API docs will be available at: http://localhost:8000/docs
```

### Step 3: Test the Service (New Terminal)

```bash
cd game-client/cli
pip install httpx
python test_client.py
```

You should see predictions working!

## 📖 Detailed Setup

### Prerequisites

- Python 3.9 or higher
- The Puckcast model project in `../puckcast`
- 5-10 minutes

### Option A: Automatic Setup (Mac/Linux)

```bash
./scripts/setup.sh
```

### Option B: Manual Setup (All Platforms)

#### 1. Set up Intelligence Service

```bash
cd intelligence-service

# Create virtual environment
python -m venv venv

# Activate (choose your platform)
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt
```

#### 2. Verify Puckcast Connection

The intelligence service needs to find the Puckcast model. It expects:
```
C:\Users\rhine\New folder (2)\
├── nhl-simulation-game/    ← You are here
└── puckcast/               ← Model should be here
    └── src/nhl_prediction/
```

If your Puckcast is elsewhere, update the path in:
`intelligence-service/src/model_client/puckcast_client.py`

```python
# Line 10 - adjust if needed
PUCKCAST_PATH = Path(__file__).parent.parent.parent.parent.parent / 'puckcast'
```

#### 3. Start the Service

```bash
# From intelligence-service/ with venv activated
python src/main.py
```

The service will:
1. Load the Puckcast model
2. Start the API server on port 8000
3. Show "✅ Model loaded successfully"

#### 4. Test It

Open a new terminal:

```bash
cd game-client/cli
pip install httpx
python test_client.py
```

Expected output:
```
🏒 NHL Intelligence Service - Test Client

================================
Testing Health Endpoint
================================

✅ Service is healthy
   Model version: 1.0.0
   Status: healthy

================================
Testing Game Prediction
================================

Scenario: Close game in 3rd period
  Boston (home) vs Toronto (away)
  Score: 2 - 2
  Time: 5.0 min remaining in period 3

✅ Prediction received:
   Home win probability: 57.5%
   Away win probability: 42.5%
   Expected goals (home): 4.75
   Expected goals (away): 4.75
   Confidence: 75.0%
   Model version: 1.0.0
```

## 🧪 Try the API Yourself

### Open the Interactive Docs

Visit: http://localhost:8000/docs

This shows all API endpoints with a "Try it out" button!

### Example: Predict a Game

POST to `http://localhost:8000/predict-game`

```json
{
  "home_team_id": 6,
  "away_team_id": 10,
  "period": 3,
  "time_remaining": 5.0,
  "score_home": 2,
  "score_away": 2
}
```

Response:
```json
{
  "home_win_prob": 0.575,
  "away_win_prob": 0.425,
  "expected_goals_home": 4.75,
  "expected_goals_away": 4.75,
  "confidence": 0.75,
  "model_version": "1.0.0"
}
```

## 🎮 Next Steps

### Week 1: You Are Here
- ✅ Intelligence service running
- ✅ Can query predictions
- 🎯 Next: Build game simulator

### Week 2: Game Engine
Create the actual game simulation in `game-engine/`:

```python
from intelligence_client import IntelligenceClient

class GameSimulator:
    def __init__(self):
        self.ai = IntelligenceClient("http://localhost:8000")
    
    def simulate_game(self, home, away):
        # Query AI for predictions
        result = self.ai.predict_game({
            'home_team_id': home,
            'away_team_id': away,
            # ...
        })
        
        # Simulate based on predictions
        # ...
```

### Week 3: Web Interface
Create a web UI in `game-client/web/`:
- Next.js app
- Game simulation UI
- Real-time updates

### Week 4: Polish & Launch
- Add more features
- Test with users
- Deploy!

## 🐛 Troubleshooting

### Error: "Cannot find puckcast module"

**Problem:** Intelligence service can't find the Puckcast model.

**Solution:** Check the path in `puckcast_client.py`:
```python
PUCKCAST_PATH = Path(__file__).parent.parent.parent.parent.parent / 'puckcast'
```

Make sure `../puckcast/src/nhl_prediction/` exists.

### Error: "Address already in use"

**Problem:** Port 8000 is already taken.

**Solution:** Change port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

### Error: "Model failed to load"

**Problem:** Puckcast model data is missing.

**Solution:** 
1. Check if `../puckcast/data/` exists
2. Run Puckcast's data fetch script first
3. Check error messages for specific issues

## 📚 Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - How everything fits together
- **[API Reference](docs/API_REFERENCE.md)** - Full API documentation
- **[Game Design](docs/GAME_DESIGN.md)** - Gameplay mechanics

## 💬 Need Help?

1. Check if intelligence service is running: http://localhost:8000/health
2. Check API docs: http://localhost:8000/docs
3. Run test client: `python game-client/cli/test_client.py`
4. Check logs in terminal where service is running

## 🎯 Success Checklist

- [ ] Intelligence service starts without errors
- [ ] Health endpoint returns "healthy"
- [ ] Test client runs successfully
- [ ] Can see predictions in API docs
- [ ] Ready to build game engine!

---

**Next:** Build the game simulator in `game-engine/`

See [BUILD_ROADMAP.md](BUILD_ROADMAP.md) for the full 4-week plan.

