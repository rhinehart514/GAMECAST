"""
Game API Server

REST API for NHL game and season simulation.
Provides endpoints for the web UI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add game-engine to path
game_engine_path = Path(__file__).parent.parent / "game-engine"
sys.path.insert(0, str(game_engine_path))

from simulator import NHLSimulator
from season_simulator import SeasonSimulator, TeamRecord
from playoff_simulator import PlayoffSimulator, PlayoffBracket
from gm_career import GMCareerManager, GMCareer
from nhl_loader import load_all_teams
from nhl_data import NHL_TEAMS, NHLTeam

# Initialize
app = FastAPI(title="NHL Simulation API", version="1.0.0")

# CORS for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load teams on startup
load_all_teams()
game_simulator = NHLSimulator(verbose=False)
active_seasons: Dict[str, SeasonSimulator] = {}
active_playoffs: Dict[str, PlayoffSimulator] = {}
gm_manager = GMCareerManager()


# Models
class TeamInfo(BaseModel):
    code: str
    name: str
    city: str
    division: str
    conference: str
    overall_strength: float
    wins: int
    losses: int
    otl: int


class GoalEvent(BaseModel):
    period: int
    time_elapsed: int
    team: str
    scorer: Optional[str]
    scorer_id: Optional[int]
    primary_assist: Optional[str]
    secondary_assist: Optional[str]
    is_power_play: bool
    is_empty_net: bool


class PeriodSummary(BaseModel):
    period: int
    home_goals: int
    away_goals: int
    goals: List[GoalEvent]


class GameResult(BaseModel):
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    winner: Optional[str]
    periods: int
    home_shots: int
    away_shots: int
    period_scores: Dict[str, PeriodSummary]
    goal_scorers: List[str]  # List of all goal scorers for quick reference


class SeasonStandings(BaseModel):
    team_code: str
    team_name: str
    games_played: int
    wins: int
    losses: int
    otl: int
    points: int
    goals_for: int
    goals_against: int
    goal_differential: int
    points_percentage: float


# Endpoints
@app.get("/")
def root():
    return {
        "service": "NHL Simulation API",
        "version": "1.0.0",
        "endpoints": {
            "teams": "/teams",
            "simulate_game": "/game/simulate",
            "season_create": "/season/create",
            "season_simulate": "/season/{season_id}/simulate",
            "season_standings": "/season/{season_id}/standings"
        }
    }


@app.get("/teams", response_model=List[TeamInfo])
def get_teams():
    """Get all NHL teams."""
    teams = []
    for code, team in NHL_TEAMS.items():
        teams.append(TeamInfo(
            code=code,
            name=team.name,
            city=team.city,
            division=team.division,
            conference=team.conference,
            overall_strength=team.overall_strength,
            wins=team.stats.wins,
            losses=team.stats.losses,
            otl=team.stats.otl
        ))
    return sorted(teams, key=lambda t: t.overall_strength, reverse=True)


@app.post("/game/simulate", response_model=GameResult)
def simulate_game(home_team: str, away_team: str):
    """Simulate a single game with full player attribution."""
    if home_team not in NHL_TEAMS:
        raise HTTPException(status_code=404, detail=f"Team {home_team} not found")
    if away_team not in NHL_TEAMS:
        raise HTTPException(status_code=404, detail=f"Team {away_team} not found")
    
    game = game_simulator.simulate_game(away_team, home_team)
    winner = game.get_winner()
    
    # Extract period-by-period scoring
    period_scores = {}
    all_goal_scorers = []
    
    for period_num, period_score in game.period_scores.items():
        goals = []
        for goal_info in period_score.goals:
            if goal_info.get('scorer'):
                all_goal_scorers.append(goal_info['scorer'])
            
            goals.append(GoalEvent(
                period=period_num,
                time_elapsed=goal_info.get('time_elapsed', 0),
                team=goal_info.get('team', ''),
                scorer=goal_info.get('scorer'),
                scorer_id=goal_info.get('scorer_id'),
                primary_assist=goal_info.get('primary_assist'),
                secondary_assist=goal_info.get('secondary_assist'),
                is_power_play=goal_info.get('is_power_play', False),
                is_empty_net=goal_info.get('is_empty_net', False)
            ))
        
        period_scores[str(period_num)] = PeriodSummary(
            period=period_num,
            home_goals=period_score.home_goals,
            away_goals=period_score.away_goals,
            goals=goals
        )
    
    return GameResult(
        home_team=home_team,
        away_team=away_team,
        home_score=game.home_team.score,
        away_score=game.away_team.score,
        winner=winner.code if winner else None,
        periods=game.period.value,
        home_shots=game.home_team.shots,
        away_shots=game.away_team.shots,
        period_scores=period_scores,
        goal_scorers=all_goal_scorers
    )


@app.post("/season/create")
def create_season(season_year: str = "2024-25"):
    """Create a new season."""
    season_id = f"season_{len(active_seasons) + 1}"
    active_seasons[season_id] = SeasonSimulator(season_year=season_year, verbose=False)
    
    return {
        "season_id": season_id,
        "season_year": season_year,
        "total_games": len(active_seasons[season_id].schedule),
        "status": "created"
    }


@app.post("/season/{season_id}/simulate")
def simulate_season(season_id: str, num_games: int = 10):
    """Simulate games in a season."""
    if season_id not in active_seasons:
        raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
    
    season = active_seasons[season_id]
    season.simulate_season(num_games=num_games)
    
    games_played = sum(1 for g in season.schedule if g.played)
    
    return {
        "season_id": season_id,
        "games_simulated": num_games,
        "total_games_played": games_played,
        "total_games": len(season.schedule),
        "status": "in_progress" if games_played < len(season.schedule) else "complete"
    }


@app.get("/season/{season_id}/standings", response_model=List[SeasonStandings])
def get_season_standings(season_id: str, conference: Optional[str] = None):
    """Get season standings."""
    if season_id not in active_seasons:
        raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
    
    season = active_seasons[season_id]
    standings = []
    
    for code, record in season.records.items():
        team = NHL_TEAMS[code]
        
        if conference and team.conference != conference:
            continue
        
        standings.append(SeasonStandings(
            team_code=code,
            team_name=record.team_name,
            games_played=record.games_played,
            wins=record.wins,
            losses=record.losses,
            otl=record.otl,
            points=record.points,
            goals_for=record.goals_for,
            goals_against=record.goals_against,
            goal_differential=record.goal_differential,
            points_percentage=record.points_percentage
        ))
    
    # Sort by points, then goal differential
    standings.sort(key=lambda s: (s.points, s.goal_differential), reverse=True)
    
    return standings


@app.get("/season/{season_id}/games")
def get_season_games(season_id: str, played_only: bool = False):
    """Get games from a season."""
    if season_id not in active_seasons:
        raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
    
    season = active_seasons[season_id]
    games = []
    
    for game in season.schedule:
        if played_only and not game.played:
            continue
        
        games.append({
            "home_team": game.home_team,
            "away_team": game.away_team,
            "date": game.date.isoformat(),
            "played": game.played,
            "home_score": game.home_score if game.played else None,
            "away_score": game.away_score if game.played else None,
            "overtime": game.overtime if game.played else None
        })
    
    return {"season_id": season_id, "games": games}


# Playoff Endpoints
@app.post("/season/{season_id}/playoffs/generate")
def generate_playoffs(season_id: str):
    """Generate playoff bracket from season standings."""
    if season_id not in active_seasons:
        raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
    
    season = active_seasons[season_id]
    
    # Get standings with conference info
    standings = []
    for code, record in season.records.items():
        team = NHL_TEAMS[code]
        standings.append({
            "team_code": code,
            "team_name": record.team_name,
            "points": record.points,
            "goal_differential": record.goal_differential,
            "conference": team.conference
        })
    
    # Create playoff simulator and generate bracket
    playoff_sim = PlayoffSimulator(season_year=season.season_year, verbose=False)
    bracket = playoff_sim.generate_bracket(standings)
    
    # Store playoff simulator
    playoff_id = f"playoff_{season_id}"
    active_playoffs[playoff_id] = playoff_sim
    
    return {
        "playoff_id": playoff_id,
        "season_id": season_id,
        "bracket": bracket.to_dict(),
        "status": "generated"
    }


@app.post("/playoffs/{playoff_id}/simulate/round")
def simulate_playoff_round(playoff_id: str, round_number: int):
    """Simulate a specific playoff round."""
    if playoff_id not in active_playoffs:
        raise HTTPException(status_code=404, detail=f"Playoffs {playoff_id} not found")
    
    playoff_sim = active_playoffs[playoff_id]
    
    if not playoff_sim.bracket:
        raise HTTPException(status_code=400, detail="No bracket generated")
    
    # Validate round number
    if round_number < 1 or round_number > 4:
        raise HTTPException(status_code=400, detail="Round must be 1-4")
    
    from playoff_simulator import Round
    round_enum = Round(round_number)
    
    # Simulate the round
    success = playoff_sim.simulate_round(round_enum)
    
    if not success:
        raise HTTPException(status_code=400, detail=f"No series to simulate in round {round_number}")
    
    return {
        "playoff_id": playoff_id,
        "round": round_number,
        "bracket": playoff_sim.bracket.to_dict(),
        "status": "completed" if playoff_sim.bracket.champion else "in_progress"
    }


@app.post("/playoffs/{playoff_id}/simulate/all")
def simulate_all_playoffs(playoff_id: str):
    """Simulate entire playoffs from current state to Stanley Cup."""
    if playoff_id not in active_playoffs:
        raise HTTPException(status_code=404, detail=f"Playoffs {playoff_id} not found")
    
    playoff_sim = active_playoffs[playoff_id]
    
    if not playoff_sim.bracket:
        raise HTTPException(status_code=400, detail="No bracket generated")
    
    # Simulate all remaining rounds
    bracket = playoff_sim.simulate_playoffs()
    
    return {
        "playoff_id": playoff_id,
        "bracket": bracket.to_dict(),
        "champion": bracket.champion,
        "status": "completed"
    }


@app.get("/playoffs/{playoff_id}/bracket")
def get_playoff_bracket(playoff_id: str):
    """Get current state of playoff bracket."""
    if playoff_id not in active_playoffs:
        raise HTTPException(status_code=404, detail=f"Playoffs {playoff_id} not found")
    
    playoff_sim = active_playoffs[playoff_id]
    
    if not playoff_sim.bracket:
        raise HTTPException(status_code=404, detail="No bracket generated")
    
    return {
        "playoff_id": playoff_id,
        "bracket": playoff_sim.bracket.to_dict(),
        "champion": playoff_sim.bracket.champion,
        "status": "completed" if playoff_sim.bracket.champion else "in_progress"
    }


# Player Stats Endpoints
@app.get("/season/{season_id}/stats/leaders")
def get_league_leaders(
    season_id: str,
    stat: str = "points",
    limit: int = 10,
    min_games: int = 10
):
    """Get league leaders for a specific stat."""
    if season_id not in active_seasons:
        raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
    
    season = active_seasons[season_id]
    leaders = season.stats_tracker.get_league_leaders(stat=stat, limit=limit, min_games=min_games)
    
    return {
        "season_id": season_id,
        "stat": stat,
        "limit": limit,
        "min_games": min_games,
        "leaders": [player.to_dict() for player in leaders]
    }


@app.get("/season/{season_id}/stats/team/{team_code}")
def get_team_player_stats(season_id: str, team_code: str):
    """Get player stats for a specific team."""
    if season_id not in active_seasons:
        raise HTTPException(status_code=404, detail=f"Season {season_id} not found")
    
    if team_code not in NHL_TEAMS:
        raise HTTPException(status_code=404, detail=f"Team {team_code} not found")
    
    season = active_seasons[season_id]
    team_stats = season.stats_tracker.get_team_stats(team_code)
    
    return {
        "season_id": season_id,
        "team_code": team_code,
        "team_name": NHL_TEAMS[team_code].full_name,
        "players": [player.to_dict() for player in team_stats]
    }


# GM Career Mode Endpoints
@app.post("/gm/create")
def create_gm_career(gm_name: str, team_code: str, season_year: str = "2024-25"):
    """Create a new GM career."""
    try:
        career = gm_manager.create_career(gm_name, team_code, season_year)
        return {
            "career_id": career.career_id,
            "gm_name": career.gm_name,
            "team_code": career.team_code,
            "team_name": NHL_TEAMS[career.team_code].full_name,
            "season_year": career.current_season,
            "status": "created"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/gm/{career_id}")
def get_gm_career(career_id: str):
    """Get GM career details."""
    try:
        summary = gm_manager.get_career_summary(career_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/gm/{career_id}/roster")
def get_gm_roster(career_id: str):
    """Get roster for GM's team."""
    career = gm_manager.get_career(career_id)
    if not career:
        raise HTTPException(status_code=404, detail=f"Career {career_id} not found")
    
    try:
        roster = gm_manager.get_team_roster(career.team_code)
        return {
            "career_id": career_id,
            "team_code": career.team_code,
            "team_name": NHL_TEAMS[career.team_code].full_name,
            "roster": roster
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/gm/{career_id}/player/{player_id}")
def update_player_rating(
    career_id: str,
    player_id: int,
    overall: Optional[int] = None,
    offensive: Optional[int] = None,
    defensive: Optional[int] = None
):
    """Update a player's ratings."""
    career = gm_manager.get_career(career_id)
    if not career:
        raise HTTPException(status_code=404, detail=f"Career {career_id} not found")
    
    try:
        updated_player = gm_manager.update_player_rating(
            career.team_code,
            player_id,
            overall=overall,
            offensive=offensive,
            defensive=defensive
        )
        return updated_player
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/gm/careers")
def list_gm_careers():
    """List all GM careers."""
    careers = []
    for career_id, career in gm_manager.careers.items():
        careers.append({
            "career_id": career.career_id,
            "gm_name": career.gm_name,
            "team_code": career.team_code,
            "team_name": NHL_TEAMS[career.team_code].full_name,
            "seasons_completed": career.seasons_completed,
            "championships": career.championship_count
        })
    return {"careers": careers}


if __name__ == "__main__":
    import uvicorn
    print("Starting NHL Simulation API...")
    print("API will be available at: http://localhost:8001")
    print("Documentation at: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)


