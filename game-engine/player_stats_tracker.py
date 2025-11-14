"""
Player Stats Tracker

Tracks individual player statistics across games and seasons.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import defaultdict


@dataclass
class PlayerSeasonStats:
    """Season statistics for a single player."""
    player_id: int
    player_name: str
    team_code: str
    position: str
    
    # Offensive stats
    games_played: int = 0
    goals: int = 0
    assists: int = 0
    points: int = 0
    
    # Goalie stats
    wins: int = 0
    losses: int = 0
    saves: int = 0
    goals_against: int = 0
    shutouts: int = 0
    
    # Derived stats
    @property
    def goals_per_game(self) -> float:
        """Goals per game."""
        return self.goals / self.games_played if self.games_played > 0 else 0.0
    
    @property
    def assists_per_game(self) -> float:
        """Assists per game."""
        return self.assists / self.games_played if self.games_played > 0 else 0.0
    
    @property
    def points_per_game(self) -> float:
        """Points per game."""
        return self.points / self.games_played if self.games_played > 0 else 0.0
    
    @property
    def save_percentage(self) -> float:
        """Save percentage for goalies."""
        total_shots = self.saves + self.goals_against
        return (self.saves / total_shots * 100) if total_shots > 0 else 0.0
    
    @property
    def goals_against_average(self) -> float:
        """Goals against average for goalies."""
        return (self.goals_against / self.games_played) if self.games_played > 0 else 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "team_code": self.team_code,
            "position": self.position,
            "games_played": self.games_played,
            "goals": self.goals,
            "assists": self.assists,
            "points": self.points,
            "goals_per_game": round(self.goals_per_game, 2),
            "assists_per_game": round(self.assists_per_game, 2),
            "points_per_game": round(self.points_per_game, 2),
            "wins": self.wins,
            "losses": self.losses,
            "saves": self.saves,
            "goals_against": self.goals_against,
            "shutouts": self.shutouts,
            "save_percentage": round(self.save_percentage, 3),
            "goals_against_average": round(self.goals_against_average, 2)
        }


class PlayerStatsTracker:
    """
    Tracks player statistics across games and seasons.
    """
    
    def __init__(self, season_year: str = "2024-25"):
        """Initialize stats tracker."""
        self.season_year = season_year
        self.player_stats: Dict[int, PlayerSeasonStats] = {}
        self.team_rosters: Dict[str, List[int]] = defaultdict(list)
    
    def get_or_create_player_stats(
        self, 
        player_id: int, 
        player_name: str, 
        team_code: str,
        position: str
    ) -> PlayerSeasonStats:
        """Get existing stats or create new entry for player."""
        if player_id not in self.player_stats:
            self.player_stats[player_id] = PlayerSeasonStats(
                player_id=player_id,
                player_name=player_name,
                team_code=team_code,
                position=position
            )
            self.team_rosters[team_code].append(player_id)
        return self.player_stats[player_id]
    
    def record_goal(
        self, 
        scorer_id: int, 
        scorer_name: str, 
        team_code: str,
        position: str,
        primary_assist_id: Optional[int] = None,
        primary_assist_name: Optional[str] = None,
        secondary_assist_id: Optional[int] = None,
        secondary_assist_name: Optional[str] = None
    ):
        """Record a goal and assists."""
        # Record goal
        scorer_stats = self.get_or_create_player_stats(scorer_id, scorer_name, team_code, position)
        scorer_stats.goals += 1
        scorer_stats.points += 1
        
        # Record primary assist
        if primary_assist_id and primary_assist_name:
            assist_stats = self.get_or_create_player_stats(
                primary_assist_id, primary_assist_name, team_code, "F"  # Default to forward
            )
            assist_stats.assists += 1
            assist_stats.points += 1
        
        # Record secondary assist
        if secondary_assist_id and secondary_assist_name:
            assist_stats = self.get_or_create_player_stats(
                secondary_assist_id, secondary_assist_name, team_code, "F"
            )
            assist_stats.assists += 1
            assist_stats.points += 1
    
    def record_game_participation(self, player_id: int, player_name: str, team_code: str, position: str):
        """Record that a player participated in a game."""
        stats = self.get_or_create_player_stats(player_id, player_name, team_code, position)
        stats.games_played += 1
    
    def get_league_leaders(
        self, 
        stat: str = "points", 
        limit: int = 10,
        min_games: int = 10
    ) -> List[PlayerSeasonStats]:
        """
        Get league leaders for a specific stat.
        
        Args:
            stat: Stat to sort by (goals, assists, points, etc.)
            limit: Number of players to return
            min_games: Minimum games played to qualify
            
        Returns:
            List of PlayerSeasonStats sorted by the stat
        """
        # Filter players by min games
        qualified = [p for p in self.player_stats.values() if p.games_played >= min_games]
        
        # Sort by stat
        if stat == "goals":
            qualified.sort(key=lambda p: (p.goals, p.points), reverse=True)
        elif stat == "assists":
            qualified.sort(key=lambda p: (p.assists, p.points), reverse=True)
        elif stat == "points":
            qualified.sort(key=lambda p: (p.points, p.goals), reverse=True)
        elif stat == "goals_per_game":
            qualified.sort(key=lambda p: (p.goals_per_game, p.goals), reverse=True)
        elif stat == "save_percentage":
            # Filter goalies
            qualified = [p for p in qualified if p.position == "G"]
            qualified.sort(key=lambda p: p.save_percentage, reverse=True)
        elif stat == "wins":
            qualified = [p for p in qualified if p.position == "G"]
            qualified.sort(key=lambda p: (p.wins, p.save_percentage), reverse=True)
        else:
            qualified.sort(key=lambda p: p.points, reverse=True)
        
        return qualified[:limit]
    
    def get_team_stats(self, team_code: str) -> List[PlayerSeasonStats]:
        """Get all player stats for a specific team."""
        player_ids = self.team_rosters.get(team_code, [])
        team_stats = [self.player_stats[pid] for pid in player_ids if pid in self.player_stats]
        team_stats.sort(key=lambda p: p.points, reverse=True)
        return team_stats
    
    def get_all_players(self) -> List[PlayerSeasonStats]:
        """Get all player stats."""
        return list(self.player_stats.values())
    
    def to_dict(self) -> Dict:
        """Convert all stats to dictionary."""
        return {
            "season_year": self.season_year,
            "total_players": len(self.player_stats),
            "players": {pid: stats.to_dict() for pid, stats in self.player_stats.items()}
        }


