# NHL Simulation Game 🏒

A sophisticated NHL game simulator powered by machine learning. Simulate individual games or entire seasons with real NHL team data, AI-driven decision-making, and beautiful dark mode UI.

## Features

- **🤖 AI-Driven Gameplay**: Machine learning model guides every simulation for realistic outcomes
- **📊 Real NHL Data**: All 32 NHL teams with actual rosters, player ratings, and season stats
- **⚡ Living Game Architecture**: ML model continuously improves the simulation quality
- **🎮 Game Mode**: Simulate individual matchups between any two teams
- **🏆 Season Mode**: Run full 82-game seasons and track standings
- **🎯 GM Mode**: Manage your own NHL team, edit rosters, and build a dynasty
- **🏒 Playoff Simulator**: Complete bracket system with best-of-7 series and Stanley Cup Finals
- **📈 Analytics Dashboard**: League leaders, player stats, sortable tables with filters
- **👥 Roster Management**: Edit player ratings and customize team strength
- **👤 Player-Level Attribution**: See who scored, who assisted, with realistic stat distribution
- **⏱️ Period-by-Period Breakdown**: Track scoring by period with timestamps
- **🌙 Beautiful Dark UI**: Apple-inspired design with glass morphism effects
- **📊 Real-time Stats**: Track goals, shots, player events, and league-wide performance

## Architecture

```
┌─────────────────┐
│   Web UI        │  Next.js 15 + React + Tailwind
│   (Port 3000)   │  Dark mode interface with glassmorphism
└────────┬────────┘
         │
         ├─────────────────────────────────────┐
         │                                     │
┌────────▼────────┐               ┌───────────▼──────────┐
│   Game API      │               │ Intelligence Service │
│   (Port 8001)   │◄──────────────┤   (Port 5001)       │
│   FastAPI       │               │   FastAPI + ML      │
└────────┬────────┘               └─────────────────────┘
         │
┌────────▼────────┐
│  Game Engine    │  Python simulation engine
│  + NHL Data     │  32 teams, 700+ players
└─────────────────┘
```

## Tech Stack

- **Backend**:
  - Python 3.10+
  - FastAPI for REST APIs
  - ML model for predictions
  - Real NHL team data

- **Frontend**:
  - Next.js 15 (App Router)
  - React 19
  - TypeScript
  - Tailwind CSS
  - Glassmorphism UI

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PowerShell (Windows)

### 1. Install Dependencies

**Game Engine & API:**
```powershell
cd game-engine
pip install -r requirements.txt
cd ../game-api
pip install -r requirements.txt
```

**Intelligence Service:**
```powershell
cd intelligence-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Web UI:**
```powershell
cd web-ui
npm install
```

### 2. Start All Services

**Easy way (Recommended):**
```powershell
.\START_ALL_SERVICES.ps1
```

**Manual way:**

```powershell
# Terminal 1 - Intelligence Service (ML Model)
cd intelligence-service
.\venv\Scripts\Activate.ps1
cd src
python main.py

# Terminal 2 - Game API
cd game-api
python main.py

# Terminal 3 - Web UI
cd web-ui
npm run dev
```

### 3. Access the Application

- 🌐 **Web UI**: http://localhost:3000
- 🎮 **Game API**: http://localhost:8001/docs
- 🧠 **Intelligence Service**: http://localhost:5001/docs

## Usage

### Game Mode

1. Click **Game Mode** on the home screen
2. Select a home team and away team
3. Click **Simulate Game**
4. Watch the ML-guided simulation run (30-60 seconds)
5. View detailed results:
   - Final score with period-by-period breakdown
   - **Player-level goal attribution** (scorer + assists)
   - Timestamps for each goal (MM:SS)
   - Power play and empty net indicators
   - Shot statistics

### Season Mode

1. Click **Season Mode** on the home screen
2. Create a new season (e.g., "2024-25")
3. Simulate games in batches:
   - +10 Games
   - +1 Week (82 games)
   - +1 Month (328 games)
   - Complete Season (all remaining games)
4. View live standings with playoff positions
5. Filter by conference (Eastern/Western)

### Analytics Dashboard

1. Navigate to **Analytics** tab in Season Mode
2. View league leaders by:
   - Points
   - Goals
   - Assists
   - Goals per Game
3. Filter by team
4. See top scorers, playmakers, and stat summaries
5. Track performance across 10-100+ players

### Playoff Mode

1. Complete at least 80% of season
2. Navigate to **Playoffs** tab
3. Click **Generate Bracket** to create matchups
4. Simulate individual rounds or all at once:
   - Round 1 (8 series per conference)
   - Round 2 (4 series per conference)
   - Conference Finals (2 series)
   - Stanley Cup Finals
5. Watch series progress with game-by-game results
6. See Stanley Cup Champion crowned! 🏆

### GM Mode 🎯

1. Click **GM Mode** on the home screen
2. Enter your name
3. Select a team to manage (all 32 NHL teams available)
4. Click **Start GM Career**
5. View career dashboard:
   - Career stats (W-L-OTL, win %)
   - Playoff appearances
   - Championships won
   - Team information
6. Navigate to **Roster** tab
7. Edit player ratings:
   - Overall rating (0-100)
   - Offensive rating (0-100)
   - Defensive rating (0-100)
8. Build your championship roster!
9. Use your customized team in Season Mode

## API Endpoints

### Game API (`http://localhost:8001`)

**Game & Season:**
- `GET /teams` - Get all NHL teams
- `POST /game/simulate?home_team={code}&away_team={code}` - Simulate a game
- `POST /season/create?season_year={year}` - Create a new season
- `POST /season/{id}/simulate?num_games={n}` - Simulate season games
- `GET /season/{id}/standings` - Get season standings
- `GET /season/{id}/games` - Get all season games

**Playoffs:**
- `POST /season/{id}/playoffs/generate` - Generate playoff bracket
- `POST /playoffs/{id}/simulate/round?round_number={n}` - Simulate a round
- `POST /playoffs/{id}/simulate/all` - Simulate all playoffs
- `GET /playoffs/{id}/bracket` - Get bracket status

**Analytics:**
- `GET /season/{id}/stats/leaders?stat={type}&limit={n}` - Get league leaders
- `GET /season/{id}/stats/team/{code}` - Get team player stats

**GM Mode:**
- `POST /gm/create?gm_name={name}&team_code={code}` - Create GM career
- `GET /gm/{career_id}` - Get career details
- `GET /gm/{career_id}/roster` - Get team roster
- `PUT /gm/{career_id}/player/{player_id}` - Update player ratings
- `GET /gm/careers` - List all GM careers

### Intelligence Service (`http://localhost:5001`)

- `POST /intelligence/predict` - Get ML prediction for a game
- `POST /intelligence/goalie-pull` - Decide when to pull goalie
- `GET /health` - Service health check

## Project Structure

```
nhl-simulation-game/
├── game-engine/          # Core simulation engine
│   ├── simulator.py      # Game simulation logic
│   ├── nhl_data.py       # NHL team data models
│   ├── nhl_loader.py     # Team data loading
│   └── season_simulator.py # Season simulation
├── game-api/             # REST API for game engine
│   └── main.py           # FastAPI app
├── intelligence-service/ # ML service
│   └── src/
│       ├── main.py       # FastAPI app
│       └── model_client/ # ML model integration
├── web-ui/               # Next.js frontend
│   ├── app/              # App router pages
│   ├── components/       # React components
│   └── lib/              # API client
├── START_ALL_SERVICES.ps1 # Easy startup script
└── STOP_ALL_SERVICES.ps1  # Easy shutdown script
```

## Development

### Testing Game Simulation

```powershell
cd game-engine
python test_ml_guided.py
```

### Testing Season Simulation

```powershell
cd game-engine
python -c "from season_simulator import NHLSeasonSimulator; s = NHLSeasonSimulator('2024-25'); s.simulate_games(10); print(s.get_standings()[:5])"
```

### Building for Production

```powershell
cd web-ui
npm run build
npm start
```

## Key Features Explained

### ML-Guided Simulation

The game engine queries the Intelligence Service before each game to get:
- **Win probability** for each team
- **Expected goals** for each team
- **Strategic decisions** (goalie pulls, line changes)

The simulation then dynamically adjusts shot success rates to align with ML predictions while maintaining realistic play-by-play action.

### Living Game Architecture

The ML model can be retrained and improved without touching the game engine code. As the model gets better, simulations automatically become more realistic.

### Real NHL Data

- **32 Teams**: All current NHL teams
- **700+ Players**: Real rosters with positions and ratings
- **Team Stats**: Goals for/against, power play %, penalty kill %
- **Player Ratings**: Overall skill (0-100), offensive/defensive strengths

### Home Ice Advantage

Home teams receive a 5% boost to offensive capabilities and 3% boost to defensive capabilities, simulating real home-ice advantage.

## Stopping Services

```powershell
.\STOP_ALL_SERVICES.ps1
```

Or press `Ctrl+C` in each terminal window if running manually.

## Troubleshooting

**Services won't start:**
- Check if ports 3000, 5001, 8001 are available
- Run `STOP_ALL_SERVICES.ps1` first to clean up

**API connection errors:**
- Ensure all three services are running
- Check firewall settings
- Verify `.env.local` in web-ui has correct API URL

**Simulation is slow:**
- Normal! ML-guided games take 30-60 seconds
- Running in verbose mode is slower
- Season simulation can take several minutes

## Completed Features ✅

- **GM Mode** - Manage teams, edit rosters, build dynasties
- **Player-level event attribution** - See who scored, who assisted, timestamps
- **Playoff bracket simulation** - Complete best-of-7 series with Stanley Cup Finals
- **Advanced analytics dashboard** - League leaders, sortable stats, filters
- **Player stat tracking** - Goals, assists, points across seasons
- **Roster management** - Edit player ratings and team composition

## Future Enhancements

- [ ] Penalty simulation with player attribution
- [ ] Enhanced overtime/shootout details with shooters
- [ ] Historical season replay with real data
- [ ] Individual game details from season (click to view)
- [ ] Career mode with multi-season tracking
- [ ] Mobile responsive design optimization
- [ ] Team customization (edit rosters, ratings)
- [ ] Export season results to CSV/JSON
- [ ] Playoff series game logs with detailed stats
- [ ] Head-to-head team comparisons

## License

MIT License - see LICENSE file for details

## Credits

Built with modern web technologies and machine learning. All NHL team names, logos, and trademarks are property of their respective organizations. This is a simulation project for educational purposes.

---

**Enjoy simulating hockey! 🏒🚀**
