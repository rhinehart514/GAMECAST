"""
GM Career Mode

Manages a General Manager career where you control one team across multiple seasons.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json

from nhl_data import NHLTeam, NHL_TEAMS, Player


@dataclass
class GMCareer:
    """GM career tracking."""
    career_id: str
    gm_name: str
    team_code: str
    current_season: str
    seasons_completed: int = 0
    
    # Career stats
    total_wins: int = 0
    total_losses: int = 0
    total_otl: int = 0
    playoff_appearances: int = 0
    championships: List[str] = field(default_factory=list)
    
    # Season history
    season_records: Dict[str, Dict] = field(default_factory=dict)
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def win_percentage(self) -> float:
        """Calculate career win percentage."""
        total_games = self.total_wins + self.total_losses + self.total_otl
        return (self.total_wins / total_games * 100) if total_games > 0 else 0.0
    
    @property
    def championship_count(self) -> int:
        """Number of championships won."""
        return len(self.championships)
    
    def add_season_record(self, season_year: str, wins: int, losses: int, otl: int, 
                         made_playoffs: bool, won_championship: bool = False):
        """Add a completed season to career history."""
        self.season_records[season_year] = {
            "wins": wins,
            "losses": losses,
            "otl": otl,
            "points": wins * 2 + otl,
            "made_playoffs": made_playoffs,
            "won_championship": won_championship
        }
        
        self.total_wins += wins
        self.total_losses += losses
        self.total_otl += otl
        self.seasons_completed += 1
        
        if made_playoffs:
            self.playoff_appearances += 1
        
        if won_championship:
            self.championships.append(season_year)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "career_id": self.career_id,
            "gm_name": self.gm_name,
            "team_code": self.team_code,
            "team_name": NHL_TEAMS[self.team_code].full_name if self.team_code in NHL_TEAMS else "Unknown",
            "current_season": self.current_season,
            "seasons_completed": self.seasons_completed,
            "total_wins": self.total_wins,
            "total_losses": self.total_losses,
            "total_otl": self.total_otl,
            "win_percentage": round(self.win_percentage, 2),
            "playoff_appearances": self.playoff_appearances,
            "championship_count": self.championship_count,
            "championships": self.championships,
            "season_records": self.season_records,
            "created_at": self.created_at
        }


class GMCareerManager:
    """
    Manages GM career mode.
    
    Handles team selection, roster management, and career tracking.
    """
    
    def __init__(self):
        """Initialize GM career manager."""
        self.careers: Dict[str, GMCareer] = {}
    
    def create_career(self, gm_name: str, team_code: str, season_year: str = "2024-25") -> GMCareer:
        """
        Create a new GM career.
        
        Args:
            gm_name: Name of the GM
            team_code: Team code to manage
            season_year: Starting season
            
        Returns:
            GMCareer instance
        """
        if team_code not in NHL_TEAMS:
            raise ValueError(f"Invalid team code: {team_code}")
        
        career_id = f"gm_{len(self.careers) + 1}"
        
        career = GMCareer(
            career_id=career_id,
            gm_name=gm_name,
            team_code=team_code,
            current_season=season_year
        )
        
        self.careers[career_id] = career
        return career
    
    def get_career(self, career_id: str) -> Optional[GMCareer]:
        """Get a career by ID."""
        return self.careers.get(career_id)
    
    def get_team_roster(self, team_code: str) -> List[Dict]:
        """
        Get roster for a team.
        
        Args:
            team_code: Team code
            
        Returns:
            List of player dictionaries
        """
        if team_code not in NHL_TEAMS:
            raise ValueError(f"Invalid team code: {team_code}")
        
        team = NHL_TEAMS[team_code]
        roster = []
        
        for player in team.players:
            roster.append({
                "player_id": player.player_id,
                "name": player.name,
                "position": player.position,
                "overall_rating": player.overall,
                "offensive_rating": player.offensive,
                "defensive_rating": player.defensive
            })
        
        return sorted(roster, key=lambda p: p['overall_rating'], reverse=True)
    
    def update_player_rating(self, team_code: str, player_id: int, 
                            overall: Optional[int] = None,
                            offensive: Optional[int] = None,
                            defensive: Optional[int] = None) -> Dict:
        """
        Update a player's ratings.
        
        Args:
            team_code: Team code
            player_id: Player ID
            overall: New overall rating (0-100)
            offensive: New offensive rating (0-100)
            defensive: New defensive rating (0-100)
            
        Returns:
            Updated player data
        """
        if team_code not in NHL_TEAMS:
            raise ValueError(f"Invalid team code: {team_code}")
        
        team = NHL_TEAMS[team_code]
        player = None
        
        for p in team.players:
            if p.player_id == player_id:
                player = p
                break
        
        if not player:
            raise ValueError(f"Player {player_id} not found on team {team_code}")
        
        # Update ratings
        if overall is not None:
            player.overall = max(0, min(100, overall))
        if offensive is not None:
            player.offensive = max(0, min(100, offensive))
        if defensive is not None:
            player.defensive = max(0, min(100, defensive))
        
        return {
            "player_id": player.player_id,
            "name": player.name,
            "position": player.position,
            "overall_rating": player.overall,
            "offensive_rating": player.offensive,
            "defensive_rating": player.defensive,
            "updated": True
        }
    
    def get_career_summary(self, career_id: str) -> Dict:
        """Get comprehensive career summary."""
        career = self.get_career(career_id)
        if not career:
            raise ValueError(f"Career {career_id} not found")
        
        team = NHL_TEAMS[career.team_code]
        
        return {
            "career": career.to_dict(),
            "team": {
                "code": team.code,
                "name": team.name,
                "full_name": team.full_name,
                "city": team.city,
                "conference": team.conference,
                "division": team.division,
                "overall_strength": team.overall_strength,
                "roster_size": len(team.players)
            },
            "achievements": {
                "seasons_played": career.seasons_completed,
                "playoff_rate": round((career.playoff_appearances / career.seasons_completed * 100) 
                                     if career.seasons_completed > 0 else 0, 1),
                "championships": career.championship_count
            }
        }


if __name__ == "__main__":
    """Test GM career mode."""
    
    from nhl_loader import load_all_teams
    
    print("GM Career Mode Test")
    print("=" * 70)
    
    # Load teams
    load_all_teams()
    
    # Create GM career
    gm_manager = GMCareerManager()
    career = gm_manager.create_career("Test GM", "TOR", "2024-25")
    
    print(f"\nCreated Career: {career.gm_name} managing {NHL_TEAMS['TOR'].full_name}")
    
    # Get roster
    roster = gm_manager.get_team_roster("TOR")
    print(f"\nRoster Size: {len(roster)} players")
    print("\nTop 5 Players:")
    for player in roster[:5]:
        print(f"  {player['name']:20} {player['position']:5} Overall: {player['overall_rating']}")
    
    # Add some season history
    career.add_season_record("2024-25", 50, 28, 4, True, False)
    career.add_season_record("2025-26", 55, 22, 5, True, True)
    
    # Get summary
    summary = gm_manager.get_career_summary(career.career_id)
    print(f"\nCareer Stats:")
    print(f"  Seasons: {summary['career']['seasons_completed']}")
    print(f"  Record: {summary['career']['total_wins']}-{summary['career']['total_losses']}-{summary['career']['total_otl']}")
    print(f"  Win %: {summary['career']['win_percentage']}")
    print(f"  Playoffs: {summary['career']['playoff_appearances']}")
    print(f"  Championships: {summary['career']['championship_count']}")

