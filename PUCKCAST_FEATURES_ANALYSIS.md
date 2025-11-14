# Puckcast Model Features - Available Data

Based on analysis of the Puckcast model, here's what data we can leverage:

## Core Features Available

### Expected Goals (xG)
- `season_xg_for_avg` - Average xG for per game
- `season_xg_against_avg` - Average xG against per game
- `season_xg_diff_avg` - xG differential
- `rolling_xg_for_{window}` - Recent xG trends
- `rolling_xg_against_{window}` - Recent defensive xG
- `momentum_xg` - Hot/cold xG trends

### Possession Metrics
- `rolling_corsi_{window}` - Shot attempts for/against
- `rolling_fenwick_{window}` - Unblocked shot attempts
- `rolling_faceoff_{window}` - Faceoff win percentage

### Shooting Quality
- `rolling_high_danger_shots_{window}` - Quality scoring chances
- `shotsFor_roll_{window}` - Shots for trend
- `shotsAgainst_roll_{window}` - Shots against trend
- `shot_margin_last_game` - Recent shot differential

### Goaltending
- `rolling_save_pct_{window}` - Save percentage trends
- `rolling_gsax_{window}` - Goals saved above expected

### Game State
- `rest_days` - Days rest before game
- `is_b2b` - Back-to-back game indicator
- `games_last_3d` - Games in last 3 days
- `games_last_6d` - Games in last 6 days

### Team Form
- `season_win_pct` - Win percentage
- `momentum_win_pct` - Recent win percentage
- `rolling_win_pct_{window}` - Windowed win rate
- `season_goal_diff_avg` - Goal differential
- `momentum_goal_diff` - Recent goal differential

### Advanced
- `elo_diff_pre` - Elo rating difference
- `elo_expectation_home` - Elo-based win probability

## What We Can Add to Our Simulator

### 1. Player Fatigue System ✅
Use `rest_days`, `is_b2b`, `games_last_3d` to model player energy

### 2. Hot/Cold Streaks ✅
Use `momentum_win_pct`, `momentum_xg`, `momentum_goal_diff`

### 3. High-Danger Shots ✅
Use `rolling_high_danger_shots` to differentiate shot quality

### 4. Goalie Performance ✅
Use `rolling_save_pct`, `rolling_gsax` for realistic goalie variance

### 5. Possession-Based Sim ✅
Use `rolling_corsi`, `rolling_fenwick` for shot generation

## Implementation Plan

### Phase 1: Enhanced Predictions
- Query Puckcast for all available features
- Use xG, Corsi, high-danger shots in probabilities
- Add goalie hot/cold based on recent save%

### Phase 2: Player-Level Events
- Assign goals to actual players based on ratings
- Track player stats through season
- Show "Matthews scores!" instead of "Toronto scores!"

### Phase 3: Fatigue & Momentum
- Track games played in last 3/6 days
- Reduce performance on back-to-backs
- Boost/reduce based on momentum metrics

## Quick Wins for UI

1. Show ML prediction with confidence breakdown
2. Display team xG%, Corsi%, recent form
3. Highlight if team is on back-to-back
4. Show goalie save% trend
5. Display "hot/cold" indicators

This gives us TONS of realism without changing core architecture!



