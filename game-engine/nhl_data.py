"""
NHL Team and Player Data Models

Real NHL team data for realistic simulation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class Position(Enum):
    """Player positions."""
    CENTER = "C"
    LEFT_WING = "LW"
    RIGHT_WING = "RW"
    DEFENSEMAN = "D"
    GOALIE = "G"


@dataclass
class Player:
    """Individual player with stats."""
    id: int
    name: str
    position: Position
    number: int
    
    # Offensive stats (per 60 minutes at 5v5)
    goals_per_60: float = 0.0
    assists_per_60: float = 0.0
    points_per_60: float = 0.0
    shots_per_60: float = 0.0
    
    # Two-way stats
    corsi_for_pct: float = 50.0  # Possession %
    fenwick_for_pct: float = 50.0
    xGF_pct: float = 50.0  # Expected goals %
    
    # Goalie stats (for goalies only)
    save_pct: float = 0.900
    gaa: float = 3.00
    goals_saved_above_expected: float = 0.0
    
    # Physical
    hits_per_60: float = 0.0
    blocks_per_60: float = 0.0
    
    # Overall quality
    rating: float = 75.0  # 0-100 overall skill rating
    
    def is_goalie(self) -> bool:
        """Check if player is a goalie."""
        return self.position == Position.GOALIE
    
    def is_forward(self) -> bool:
        """Check if player is a forward."""
        return self.position in [Position.CENTER, Position.LEFT_WING, Position.RIGHT_WING]
    
    def is_defenseman(self) -> bool:
        """Check if player is a defenseman."""
        return self.position == Position.DEFENSEMAN


@dataclass
class TeamRoster:
    """Team roster organized by position."""
    centers: List[Player] = field(default_factory=list)
    left_wings: List[Player] = field(default_factory=list)
    right_wings: List[Player] = field(default_factory=list)
    defensemen: List[Player] = field(default_factory=list)
    goalies: List[Player] = field(default_factory=list)
    
    def get_all_players(self) -> List[Player]:
        """Get all players on roster."""
        return (
            self.centers + 
            self.left_wings + 
            self.right_wings + 
            self.defensemen + 
            self.goalies
        )
    
    def get_starting_goalie(self) -> Optional[Player]:
        """Get the starting goalie (highest rated)."""
        if not self.goalies:
            return None
        return max(self.goalies, key=lambda g: g.rating)
    
    def get_top_line_forwards(self) -> List[Player]:
        """Get top 3 forwards by rating."""
        forwards = self.centers + self.left_wings + self.right_wings
        return sorted(forwards, key=lambda p: p.rating, reverse=True)[:3]
    
    def get_top_defensemen(self) -> List[Player]:
        """Get top 2 defensemen by rating."""
        return sorted(self.defensemen, key=lambda p: p.rating, reverse=True)[:2]


@dataclass
class TeamStats:
    """Team-level statistics."""
    # Offensive
    goals_per_game: float = 3.0
    shots_per_game: float = 30.0
    pp_pct: float = 20.0  # Power play %
    
    # Defensive
    goals_against_per_game: float = 3.0
    shots_against_per_game: float = 30.0
    pk_pct: float = 80.0  # Penalty kill %
    
    # Possession
    corsi_for_pct: float = 50.0
    fenwick_for_pct: float = 50.0
    xGF_pct: float = 50.0
    
    # Special teams
    pp_opportunities_per_game: float = 3.0
    pk_opportunities_per_game: float = 3.0
    
    # Physical
    hits_per_game: float = 20.0
    blocks_per_game: float = 15.0
    
    # Record
    wins: int = 0
    losses: int = 0
    otl: int = 0
    
    @property
    def points(self) -> int:
        """Calculate points (W*2 + OTL*1)."""
        return self.wins * 2 + self.otl
    
    @property
    def goal_differential(self) -> float:
        """Calculate goal differential per game."""
        return self.goals_per_game - self.goals_against_per_game


@dataclass
class NHLTeam:
    """
    Complete NHL team with roster and stats.
    """
    code: str  # 3-letter code (e.g., "TOR")
    name: str  # Full name (e.g., "Toronto Maple Leafs")
    city: str  # City name
    division: str  # NHL division
    conference: str  # NHL conference
    
    roster: TeamRoster
    stats: TeamStats
    
    # Team identity
    abbreviation: str = ""
    
    def __post_init__(self):
        """Set abbreviation if not provided."""
        if not self.abbreviation:
            self.abbreviation = self.code
    
    @property
    def full_name(self) -> str:
        """Get full team name."""
        return f"{self.city} {self.name}"
    
    @property
    def offensive_strength(self) -> float:
        """
        Calculate overall offensive strength (0-100).
        Combines goals, shots, xG%, and top player ratings.
        """
        # Team stats component (70%)
        goals_normalized = min(self.stats.goals_per_game / 4.0, 1.0) * 100
        xg_normalized = self.stats.xGF_pct
        
        # Top player component (30%)
        top_forwards = self.roster.get_top_line_forwards()
        avg_forward_rating = sum(p.rating for p in top_forwards) / len(top_forwards) if top_forwards else 75
        
        return (goals_normalized * 0.4 + xg_normalized * 0.3 + avg_forward_rating * 0.3)
    
    @property
    def defensive_strength(self) -> float:
        """
        Calculate overall defensive strength (0-100).
        Combines goals against, goalie performance, and defensive ratings.
        """
        # Goals against (inverse - lower is better)
        ga_normalized = max(0, 100 - (self.stats.goals_against_per_game / 4.0) * 100)
        
        # Goalie performance
        goalie = self.roster.get_starting_goalie()
        goalie_rating = goalie.rating if goalie else 75
        
        # Defensive corps
        top_dmen = self.roster.get_top_defensemen()
        avg_dman_rating = sum(p.rating for p in top_dmen) / len(top_dmen) if top_dmen else 75
        
        return (ga_normalized * 0.4 + goalie_rating * 0.3 + avg_dman_rating * 0.3)
    
    @property
    def overall_strength(self) -> float:
        """Calculate overall team strength (0-100)."""
        return (self.offensive_strength * 0.5 + self.defensive_strength * 0.5)


# NHL Team Database - Current 2024-25 Season Data
# This will be populated by the data loader
NHL_TEAMS: Dict[str, NHLTeam] = {}


def get_team(code: str) -> Optional[NHLTeam]:
    """Get team by code."""
    return NHL_TEAMS.get(code.upper())


def get_all_teams() -> List[NHLTeam]:
    """Get all NHL teams."""
    return list(NHL_TEAMS.values())



