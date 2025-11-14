# 🚀 Quick Start Guide - Playoff & Analytics Features

## Getting Started in 3 Minutes

### 1️⃣ Access the Application

Open your browser to: **http://localhost:3000**

All services should be running:
- ✅ Web UI (Port 3000)
- ✅ Game API (Port 8001)  
- ✅ Intelligence Service (Port 5001)

---

## 🏆 Season → Analytics → Playoffs Workflow

### Step 1: Create a Season

1. Click **"Full Season"** on the home screen
2. Click **"Create Season"**
3. Enter season year (default: 2024-25)
4. Click **"Create Season 🏒"**

---

### Step 2: Simulate Games

**Quick Start (10 games for testing):**
- Click **"+10 Games"** button

**For Analytics (need 10+ games):**
- Click **"+10 Games"** or **"+1 Week (82)"**

**For Playoffs (need ~1050+ games):**
- Click **"+1 Month"** a few times
- Or click **"Complete Season"** for full simulation

⏱️ **Time Estimates:**
- 10 games: ~10 seconds
- 82 games: ~1 minute
- Full season (1312 games): ~3-5 minutes

---

### Step 3: View Standings 📊

**Default view after simulation**

Features:
- ✅ Win-Loss-OTL records
- ✅ Points and point percentage
- ✅ Goal differential
- ✅ Playoff positions marked with *
- ✅ Conference filtering (All/Eastern/Western)

---

### Step 4: Analytics Dashboard 📈

**Requirements:** 10+ games simulated

1. Click **"📈 Analytics"** tab
2. Explore features:

**League Leaders Table:**
- View top scorers, playmakers, goal scorers
- Sort by: Points, Goals, Assists, G/G
- Show: 10, 20, 50, or 100 players
- Filter by team (dropdown)
- 🥇🥈🥉 Medal indicators for top 3

**Quick Stats Cards:**
- Top scorer with point total
- Goal leader with goal count
- Assist leader with assist count

**Live Updates:**
- Click **"🔄 Refresh"** to update stats

---

### Step 5: Playoff Bracket 🏆

**Requirements:** 80%+ of season complete (~1050+ games)

1. Click **"🏆 Playoffs"** tab
2. Click **"Generate Bracket"**
3. Bracket appears with:
   - Eastern Conference seeds 1-8
   - Western Conference seeds 1-8
   - 16 total teams

**Simulation Options:**

**Individual Rounds:**
- **Simulate Round 1** - First round (8 matchups)
- **Simulate Round 2** - Second round (4 matchups)
- **Simulate Conf. Finals** - Conference finals (2 matchups)
- **Simulate Finals** - Stanley Cup Finals

**Fast Forward:**
- **⚡ Simulate All** - Complete entire playoffs at once

**Series Cards Show:**
- Team matchups (higher seed vs lower seed)
- Current series score (e.g., 2-1)
- Winner when series completes
- Round designation

---

## 🎯 Feature Highlights

### Analytics Dashboard

**What You See:**
```
Player Name     Team    GP    G    A    PTS
Connor McDavid  EDM     25    15   22   37  🥇
Nathan MacKinnon COL    24    13   19   32  🥈
Auston Matthews TOR     26    18   11   29  🥉
```

**Filtering:**
- Select stat type: Points | Goals | Assists | G/G
- Choose # players: 10 | 20 | 50 | 100
- Filter by team: All Teams | (any team code)

---

### Playoff Bracket

**Visual Structure:**
```
Eastern Conference
─────────────────
Round 1         Round 2         Conf. Finals
TOR vs TBL      Winner vs       Eastern
BOS vs NYR      Winner          Champion
```

**Series Example:**
```
┌─────────────────┐
│   Round 1       │
│  TOR  4         │  ← Winner (highlighted)
│  TBL  2         │
│  Winner: TOR 4-2│
└─────────────────┘
```

---

## 💡 Pro Tips

### For Quick Testing:
1. **Create season**
2. **Simulate 100 games** (enough for analytics)
3. **Check Analytics tab** - see league leaders
4. **Complete season** - simulate remaining games
5. **Generate playoffs** - watch for champion

### For Full Experience:
1. **Complete full season** (1312 games)
2. **Review final standings** - see playoff seeds
3. **Check analytics** - identify season leaders
4. **Generate bracket** - verify proper seeding
5. **Simulate Round 1** - watch first round
6. **Simulate remaining rounds** - or use "Simulate All"
7. **See Stanley Cup champion** 🏆

---

## 🐛 Troubleshooting

### Analytics Tab Disabled?
- Need at least **10 games** simulated
- Check progress bar shows games played

### Playoffs Tab Disabled?
- Need at least **80% of season** complete
- That's ~1050 of 1312 games
- Use "Complete Season" button for fastest results

### No Stats Showing?
- Make sure games have been simulated
- Click refresh button
- Check that Game API is running (port 8001)

### Bracket Not Generating?
- Ensure season is 80%+ complete
- Check console for errors
- Verify all services are running

---

## 🎮 Quick Commands

### Start Services:
```powershell
.\START_ALL_SERVICES.ps1
```

### Stop Services:
```powershell
.\STOP_ALL_SERVICES.ps1
```

### Check Status:
```powershell
# Web UI
curl http://localhost:3000

# Game API
curl http://localhost:8001/teams

# Intelligence
curl http://localhost:5001/health
```

---

## 📞 Support

**Services Not Running?**
1. Check if ports are in use: `netstat -ano | findstr ":3000"`
2. Restart services: `.\STOP_ALL_SERVICES.ps1` then `.\START_ALL_SERVICES.ps1`
3. Check logs in terminal windows

**API Errors?**
- Verify Python dependencies: `pip list | findstr fastapi`
- Check Intelligence Service is on port **5001** (not 8000)

**UI Not Loading?**
- Ensure `npm run dev` completed successfully
- Check browser console for errors
- Try refreshing page (Ctrl+R)

---

## 🎨 UI Navigation Map

```
Home
├── Single Game → Team Selection → Game Simulation
│
└── Full Season → Season Dashboard
    │
    ├── 📊 Standings Tab
    │   └── Conference Filter (All/East/West)
    │
    ├── 📈 Analytics Tab (10+ games)
    │   ├── Stat Category Selector
    │   ├── Player Limit Selector
    │   ├── Team Filter
    │   └── League Leaders Table
    │
    └── 🏆 Playoffs Tab (80%+ season)
        ├── Generate Bracket
        ├── Round Simulation Buttons
        ├── Conference Brackets
        └── Stanley Cup Finals
```

---

**Ready to play? Let's simulate some hockey! 🏒**

