"""
Game State Management

Tracks all game state including score, time, players, and events.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class GamePeriod(Enum):
    """Game period types."""
    FIRST = 1
    SECOND = 2
    THIRD = 3
    OVERTIME = 4
    SHOOTOUT = 5


class EventType(Enum):
    """Game event types."""
    GOAL = "goal"
    SHOT = "shot"
    SAVE = "save"
    BLOCKED_SHOT = "blocked_shot"
    MISS = "miss"
    PENALTY = "penalty"
    FACEOFF = "faceoff"
    HIT = "hit"
    GOALIE_PULL = "goalie_pull"
    GOALIE_RETURN = "goalie_return"
    LINE_CHANGE = "line_change"
    PERIOD_START = "period_start"
    PERIOD_END = "period_end"
    GAME_END = "game_end"


class StrengthSituation(Enum):
    """Game strength situations."""
    EVEN = "5v5"
    PP_MAJOR = "5v4"
    PP_MINOR = "5v3"
    SH_MAJOR = "4v5"
    SH_MINOR = "3v5"
    FOUR_ON_FOUR = "4v4"
    THREE_ON_THREE = "3v3"


@dataclass
class GameEvent:
    """Represents a single game event."""
    event_type: EventType
    period: GamePeriod
    time_remaining: int  # seconds remaining in period
    team: str  # Team code (e.g., "TOR", "BOS")
    description: str
    home_score: int
    away_score: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Player attribution (for goals, shots, saves)
    player_name: Optional[str] = None
    player_id: Optional[int] = None
    primary_assist: Optional[str] = None
    primary_assist_id: Optional[int] = None
    secondary_assist: Optional[str] = None
    secondary_assist_id: Optional[int] = None
    goalie_name: Optional[str] = None
    goalie_id: Optional[int] = None
    
    # Additional metadata
    is_power_play: bool = False
    is_empty_net: bool = False
    shot_type: Optional[str] = None  # "wrist", "slap", "snap", "backhand", "tip", "deflection"
    
    def to_dict(self) -> Dict:
        """Convert event to dictionary."""
        data = {
            "event_type": self.event_type.value,
            "period": self.period.value,
            "time_remaining": self.time_remaining,
            "team": self.team,
            "description": self.description,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "timestamp": self.timestamp.isoformat()
        }
        
        # Add player attribution if present
        if self.player_name:
            data["player_name"] = self.player_name
            data["player_id"] = self.player_id
        if self.primary_assist:
            data["primary_assist"] = self.primary_assist
            data["primary_assist_id"] = self.primary_assist_id
        if self.secondary_assist:
            data["secondary_assist"] = self.secondary_assist
            data["secondary_assist_id"] = self.secondary_assist_id
        if self.goalie_name:
            data["goalie_name"] = self.goalie_name
            data["goalie_id"] = self.goalie_id
        if self.is_power_play:
            data["is_power_play"] = self.is_power_play
        if self.is_empty_net:
            data["is_empty_net"] = self.is_empty_net
        if self.shot_type:
            data["shot_type"] = self.shot_type
        
        return data


@dataclass
class TeamState:
    """Represents a team's current state."""
    code: str  # Team abbreviation (e.g., "TOR")
    name: str  # Full name (e.g., "Toronto Maple Leafs")
    score: int = 0
    shots: int = 0
    hits: int = 0
    blocked_shots: int = 0
    faceoffs_won: int = 0
    faceoffs_lost: int = 0
    penalties: int = 0
    penalty_minutes: int = 0
    power_play_goals: int = 0
    power_play_opportunities: int = 0
    goalie_pulled: bool = False
    
    # Advanced stats (calculated during simulation)
    expected_goals: float = 0.0
    shot_attempts: int = 0
    corsi_for: int = 0
    corsi_against: int = 0
    
    def to_dict(self) -> Dict:
        """Convert team state to dictionary."""
        return {
            "code": self.code,
            "name": self.name,
            "score": self.score,
            "shots": self.shots,
            "hits": self.hits,
            "blocked_shots": self.blocked_shots,
            "faceoffs_won": self.faceoffs_won,
            "faceoffs_lost": self.faceoffs_lost,
            "penalties": self.penalties,
            "penalty_minutes": self.penalty_minutes,
            "power_play_goals": self.power_play_goals,
            "power_play_opportunities": self.power_play_opportunities,
            "goalie_pulled": self.goalie_pulled,
            "expected_goals": self.expected_goals,
            "shot_attempts": self.shot_attempts,
            "corsi_for": self.corsi_for,
            "corsi_against": self.corsi_against
        }


@dataclass
class PeriodScore:
    """Tracks scoring for a single period."""
    period: int
    home_goals: int = 0
    away_goals: int = 0
    goals: List[Dict] = field(default_factory=list)  # Detailed goal info


@dataclass
class GameState:
    """Represents the complete game state."""
    game_id: str
    home_team: TeamState
    away_team: TeamState
    period: GamePeriod = GamePeriod.FIRST
    time_remaining: int = 1200  # 20 minutes = 1200 seconds
    events: List[GameEvent] = field(default_factory=list)
    strength_situation: StrengthSituation = StrengthSituation.EVEN
    
    # Penalty tracking
    active_penalties: List[Dict] = field(default_factory=list)
    
    # Period-by-period scoring
    period_scores: Dict[int, PeriodScore] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize game start event and period scoring."""
        # Initialize period scores for regulation periods
        for period in [1, 2, 3]:
            self.period_scores[period] = PeriodScore(period=period)
        
        self.add_event(
            EventType.PERIOD_START,
            self.home_team.code,
            f"Period {self.period.value} begins"
        )
    
    def add_event(
        self, 
        event_type: EventType, 
        team: str, 
        description: str,
        player_name: Optional[str] = None,
        player_id: Optional[int] = None,
        primary_assist: Optional[str] = None,
        primary_assist_id: Optional[int] = None,
        secondary_assist: Optional[str] = None,
        secondary_assist_id: Optional[int] = None,
        goalie_name: Optional[str] = None,
        goalie_id: Optional[int] = None,
        is_power_play: bool = False,
        is_empty_net: bool = False,
        shot_type: Optional[str] = None
    ) -> GameEvent:
        """Add an event to the game log with optional player attribution."""
        event = GameEvent(
            event_type=event_type,
            period=self.period,
            time_remaining=self.time_remaining,
            team=team,
            description=description,
            home_score=self.home_team.score,
            away_score=self.away_team.score,
            player_name=player_name,
            player_id=player_id,
            primary_assist=primary_assist,
            primary_assist_id=primary_assist_id,
            secondary_assist=secondary_assist,
            secondary_assist_id=secondary_assist_id,
            goalie_name=goalie_name,
            goalie_id=goalie_id,
            is_power_play=is_power_play,
            is_empty_net=is_empty_net,
            shot_type=shot_type
        )
        self.events.append(event)
        return event
    
    def advance_time(self, seconds: int):
        """Advance game clock."""
        self.time_remaining = max(0, self.time_remaining - seconds)
        
        # Update active penalties
        self._update_penalties(seconds)
    
    def _update_penalties(self, seconds: int):
        """Update penalty timers and remove expired penalties."""
        updated_penalties = []
        for penalty in self.active_penalties:
            penalty['time_remaining'] -= seconds
            if penalty['time_remaining'] > 0:
                updated_penalties.append(penalty)
        
        self.active_penalties = updated_penalties
        self._update_strength_situation()
    
    def _update_strength_situation(self):
        """Calculate current strength situation based on active penalties."""
        home_penalties = sum(1 for p in self.active_penalties if p['team'] == self.home_team.code)
        away_penalties = sum(1 for p in self.active_penalties if p['team'] == self.away_team.code)
        
        home_skaters = 5 - home_penalties
        away_skaters = 5 - away_penalties
        
        # Handle goalie pull
        if self.home_team.goalie_pulled:
            home_skaters += 1
        if self.away_team.goalie_pulled:
            away_skaters += 1
        
        # Determine situation
        if home_skaters == 5 and away_skaters == 5:
            self.strength_situation = StrengthSituation.EVEN
        elif home_skaters == 5 and away_skaters == 4:
            self.strength_situation = StrengthSituation.PP_MAJOR
        elif home_skaters == 4 and away_skaters == 5:
            self.strength_situation = StrengthSituation.SH_MAJOR
        elif home_skaters == 4 and away_skaters == 4:
            self.strength_situation = StrengthSituation.FOUR_ON_FOUR
        elif home_skaters == 3 and away_skaters == 3:
            self.strength_situation = StrengthSituation.THREE_ON_THREE
        else:
            self.strength_situation = StrengthSituation.EVEN  # Fallback
    
    def add_penalty(self, team: str, minutes: int, description: str):
        """Add a penalty."""
        penalty = {
            'team': team,
            'time_remaining': minutes * 60,
            'description': description
        }
        self.active_penalties.append(penalty)
        
        team_state = self.home_team if team == self.home_team.code else self.away_team
        team_state.penalties += 1
        team_state.penalty_minutes += minutes
        
        self._update_strength_situation()
        self.add_event(EventType.PENALTY, team, description)
    
    def score_goal(
        self, 
        team: str, 
        is_power_play: bool = False,
        scorer_name: Optional[str] = None,
        scorer_id: Optional[int] = None,
        primary_assist: Optional[str] = None,
        primary_assist_id: Optional[int] = None,
        secondary_assist: Optional[str] = None,
        secondary_assist_id: Optional[int] = None,
        is_empty_net: bool = False,
        shot_type: Optional[str] = None
    ):
        """Record a goal with player attribution."""
        team_state = self.home_team if team == self.home_team.code else self.away_team
        team_state.score += 1
        
        if is_power_play:
            team_state.power_play_goals += 1
        
        # Build description
        description = f"GOAL! "
        if scorer_name:
            description += f"{scorer_name}"
            if primary_assist or secondary_assist:
                assists = []
                if primary_assist:
                    assists.append(primary_assist)
                if secondary_assist:
                    assists.append(secondary_assist)
                description += f" ({', '.join(assists)})"
        else:
            description += f"{team_state.name} scores"
        
        if is_power_play:
            description += " - PP"
        if is_empty_net:
            description += " - EN"
        
        # Add event
        self.add_event(
            EventType.GOAL, 
            team, 
            description,
            player_name=scorer_name,
            player_id=scorer_id,
            primary_assist=primary_assist,
            primary_assist_id=primary_assist_id,
            secondary_assist=secondary_assist,
            secondary_assist_id=secondary_assist_id,
            is_power_play=is_power_play,
            is_empty_net=is_empty_net,
            shot_type=shot_type
        )
        
        # Track period scoring
        period_num = self.period.value
        if period_num <= 3:  # Only track regulation periods in detail
            if period_num not in self.period_scores:
                self.period_scores[period_num] = PeriodScore(period=period_num)
            
            period_score = self.period_scores[period_num]
            is_home = (team == self.home_team.code)
            
            if is_home:
                period_score.home_goals += 1
            else:
                period_score.away_goals += 1
            
            # Add detailed goal info
            goal_info = {
                "team": team,
                "scorer": scorer_name,
                "scorer_id": scorer_id,
                "primary_assist": primary_assist,
                "secondary_assist": secondary_assist,
                "time_elapsed": 1200 - self.time_remaining,  # Time into period
                "is_power_play": is_power_play,
                "is_empty_net": is_empty_net
            }
            period_score.goals.append(goal_info)
    
    def advance_period(self) -> bool:
        """
        Advance to next period.
        Returns True if game continues, False if game is over.
        """
        # End current period
        self.add_event(
            EventType.PERIOD_END,
            self.home_team.code,
            f"Period {self.period.value} ends"
        )
        
        # Check if game is tied after regulation
        if self.period == GamePeriod.THIRD:
            if self.home_team.score == self.away_team.score:
                self.period = GamePeriod.OVERTIME
                self.time_remaining = 300  # 5 minute OT
                self.add_event(
                    EventType.PERIOD_START,
                    self.home_team.code,
                    "Overtime begins (3v3)"
                )
                self.strength_situation = StrengthSituation.THREE_ON_THREE
                return True
            else:
                # Game over
                self._end_game()
                return False
        
        # Check if still tied after OT
        elif self.period == GamePeriod.OVERTIME:
            if self.home_team.score == self.away_team.score:
                self.period = GamePeriod.SHOOTOUT
                self.add_event(
                    EventType.PERIOD_START,
                    self.home_team.code,
                    "Shootout begins"
                )
                return True
            else:
                self._end_game()
                return False
        
        # Advance to next regular period
        elif self.period == GamePeriod.FIRST:
            self.period = GamePeriod.SECOND
        elif self.period == GamePeriod.SECOND:
            self.period = GamePeriod.THIRD
        
        # Reset time and start new period
        self.time_remaining = 1200
        self.add_event(
            EventType.PERIOD_START,
            self.home_team.code,
            f"Period {self.period.value} begins"
        )
        return True
    
    def _end_game(self):
        """End the game."""
        winner = self.home_team if self.home_team.score > self.away_team.score else self.away_team
        self.add_event(
            EventType.GAME_END,
            winner.code,
            f"FINAL: {self.away_team.name} {self.away_team.score} - {self.home_team.score} {self.home_team.name}"
        )
    
    def is_game_over(self) -> bool:
        """Check if game is over."""
        return len(self.events) > 0 and self.events[-1].event_type == EventType.GAME_END
    
    def get_winner(self) -> Optional[TeamState]:
        """Get winning team."""
        if not self.is_game_over():
            return None
        return self.home_team if self.home_team.score > self.away_team.score else self.away_team
    
    def to_dict(self) -> Dict:
        """Convert game state to dictionary for API calls."""
        return {
            "game_id": self.game_id,
            "period": self.period.value,
            "time_remaining": self.time_remaining,
            "home_team": self.home_team.to_dict(),
            "away_team": self.away_team.to_dict(),
            "strength_situation": self.strength_situation.value,
            "active_penalties": self.active_penalties,
            "total_events": len(self.events),
            "period_scores": {
                period: {
                    "period": ps.period,
                    "home_goals": ps.home_goals,
                    "away_goals": ps.away_goals,
                    "goals": ps.goals
                }
                for period, ps in self.period_scores.items()
            }
        }
    
    def get_summary(self) -> str:
        """Get human-readable game summary."""
        mins = self.time_remaining // 60
        secs = self.time_remaining % 60
        
        summary = f"\n{'='*70}\n"
        summary += f"Period {self.period.value} - {mins:02d}:{secs:02d}\n"
        summary += f"{self.away_team.name} ({self.away_team.score}) @ {self.home_team.name} ({self.home_team.score})\n"
        summary += f"Shots: {self.away_team.shots} - {self.home_team.shots}\n"
        summary += f"Situation: {self.strength_situation.value}\n"
        summary += f"{'='*70}\n"
        
        return summary

