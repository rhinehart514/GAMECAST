"""
NHL Playoff Simulator

Handles playoff bracket generation, seeding, and best-of-7 series simulation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import random

from nhl_data import NHLTeam, get_team
from simulator import NHLSimulator


class SeriesStatus(Enum):
    """Status of a playoff series."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Round(Enum):
    """Playoff rounds."""
    FIRST_ROUND = 1
    SECOND_ROUND = 2
    CONFERENCE_FINALS = 3
    STANLEY_CUP_FINALS = 4


@dataclass
class PlayoffGame:
    """Individual playoff game result."""
    game_number: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    winner: str
    overtime: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "game_number": self.game_number,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "winner": self.winner,
            "overtime": self.overtime
        }


@dataclass
class PlayoffSeries:
    """Best-of-7 playoff series."""
    series_id: str
    round: Round
    higher_seed: str
    lower_seed: str
    higher_seed_wins: int = 0
    lower_seed_wins: int = 0
    games: List[PlayoffGame] = field(default_factory=list)
    status: SeriesStatus = SeriesStatus.NOT_STARTED
    winner: Optional[str] = None
    
    @property
    def is_complete(self) -> bool:
        """Check if series is complete (one team has 4 wins)."""
        return self.higher_seed_wins == 4 or self.lower_seed_wins == 4
    
    @property
    def games_played(self) -> int:
        """Number of games played in series."""
        return len(self.games)
    
    def get_next_home_team(self) -> str:
        """Determine home team for next game (2-2-1-1-1 format)."""
        game_num = self.games_played + 1
        
        # Games 1, 2, 5, 7 at higher seed (home)
        if game_num in [1, 2, 5, 7]:
            return self.higher_seed
        # Games 3, 4, 6 at lower seed
        else:
            return self.lower_seed
    
    def add_game_result(self, winner: str, home_score: int, away_score: int, home_team: str, away_team: str, overtime: bool = False):
        """Add a game result to the series."""
        game = PlayoffGame(
            game_number=self.games_played + 1,
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            winner=winner,
            overtime=overtime
        )
        self.games.append(game)
        
        # Update wins
        if winner == self.higher_seed:
            self.higher_seed_wins += 1
        else:
            self.lower_seed_wins += 1
        
        # Check if series is complete
        if self.is_complete:
            self.winner = winner
            self.status = SeriesStatus.COMPLETED
        else:
            self.status = SeriesStatus.IN_PROGRESS
    
    def to_dict(self) -> Dict:
        """Convert series to dictionary."""
        return {
            "series_id": self.series_id,
            "round": self.round.value,
            "higher_seed": self.higher_seed,
            "lower_seed": self.lower_seed,
            "higher_seed_wins": self.higher_seed_wins,
            "lower_seed_wins": self.lower_seed_wins,
            "games_played": self.games_played,
            "status": self.status.value,
            "winner": self.winner,
            "games": [g.to_dict() for g in self.games]
        }


@dataclass
class PlayoffBracket:
    """Complete playoff bracket for both conferences."""
    season_year: str
    eastern_conference: List[PlayoffSeries] = field(default_factory=list)
    western_conference: List[PlayoffSeries] = field(default_factory=list)
    stanley_cup_finals: Optional[PlayoffSeries] = None
    champion: Optional[str] = None
    
    def get_all_series(self) -> List[PlayoffSeries]:
        """Get all series in the bracket."""
        series = self.eastern_conference + self.western_conference
        if self.stanley_cup_finals:
            series.append(self.stanley_cup_finals)
        return series
    
    def get_active_series(self) -> List[PlayoffSeries]:
        """Get series that are in progress or not started."""
        return [s for s in self.get_all_series() if s.status != SeriesStatus.COMPLETED]
    
    def to_dict(self) -> Dict:
        """Convert bracket to dictionary."""
        return {
            "season_year": self.season_year,
            "eastern_conference": [s.to_dict() for s in self.eastern_conference],
            "western_conference": [s.to_dict() for s in self.western_conference],
            "stanley_cup_finals": self.stanley_cup_finals.to_dict() if self.stanley_cup_finals else None,
            "champion": self.champion
        }


class PlayoffSimulator:
    """
    NHL Playoff Simulator.
    
    Handles playoff bracket generation, seeding, and series simulation.
    """
    
    def __init__(self, season_year: str = "2024-25", verbose: bool = True):
        """Initialize playoff simulator."""
        self.season_year = season_year
        self.verbose = verbose
        self.game_simulator = NHLSimulator(verbose=False)  # Use quiet mode for bulk simulation
        self.bracket: Optional[PlayoffBracket] = None
    
    def generate_bracket(self, standings: List[Dict]) -> PlayoffBracket:
        """
        Generate playoff bracket from regular season standings.
        
        Args:
            standings: List of team records with points
            
        Returns:
            PlayoffBracket with seeded matchups
        """
        # Separate by conference
        eastern_teams = [s for s in standings if s['conference'] == 'Eastern']
        western_teams = [s for s in standings if s['conference'] == 'Western']
        
        # Sort by points (already sorted, but ensure)
        eastern_teams.sort(key=lambda x: (x['points'], x['goal_differential']), reverse=True)
        western_teams.sort(key=lambda x: (x['points'], x['goal_differential']), reverse=True)
        
        # Take top 8 from each conference
        eastern_playoff = eastern_teams[:8]
        western_playoff = western_teams[:8]
        
        if self.verbose:
            print("\n" + "="*80)
            print("PLAYOFF BRACKET GENERATED")
            print("="*80)
            print("\nEASTERN CONFERENCE SEEDS:")
            for i, team in enumerate(eastern_playoff, 1):
                print(f"  {i}. {team['team_name']} ({team['points']} pts)")
            
            print("\nWESTERN CONFERENCE SEEDS:")
            for i, team in enumerate(western_playoff, 1):
                print(f"  {i}. {team['team_name']} ({team['points']} pts)")
            print("="*80 + "\n")
        
        # Create bracket
        bracket = PlayoffBracket(season_year=self.season_year)
        
        # Create first round matchups
        # Eastern Conference: 1v8, 2v7, 3v6, 4v5
        bracket.eastern_conference = [
            self._create_series("E-R1-1", Round.FIRST_ROUND, eastern_playoff[0]['team_code'], eastern_playoff[7]['team_code']),
            self._create_series("E-R1-2", Round.FIRST_ROUND, eastern_playoff[1]['team_code'], eastern_playoff[6]['team_code']),
            self._create_series("E-R1-3", Round.FIRST_ROUND, eastern_playoff[2]['team_code'], eastern_playoff[5]['team_code']),
            self._create_series("E-R1-4", Round.FIRST_ROUND, eastern_playoff[3]['team_code'], eastern_playoff[4]['team_code']),
        ]
        
        # Western Conference: 1v8, 2v7, 3v6, 4v5
        bracket.western_conference = [
            self._create_series("W-R1-1", Round.FIRST_ROUND, western_playoff[0]['team_code'], western_playoff[7]['team_code']),
            self._create_series("W-R1-2", Round.FIRST_ROUND, western_playoff[1]['team_code'], western_playoff[6]['team_code']),
            self._create_series("W-R1-3", Round.FIRST_ROUND, western_playoff[2]['team_code'], western_playoff[5]['team_code']),
            self._create_series("W-R1-4", Round.FIRST_ROUND, western_playoff[3]['team_code'], western_playoff[4]['team_code']),
        ]
        
        self.bracket = bracket
        return bracket
    
    def _create_series(self, series_id: str, round: Round, higher_seed: str, lower_seed: str) -> PlayoffSeries:
        """Create a new playoff series."""
        return PlayoffSeries(
            series_id=series_id,
            round=round,
            higher_seed=higher_seed,
            lower_seed=lower_seed
        )
    
    def simulate_game(self, home_team: str, away_team: str) -> Dict:
        """Simulate a single playoff game."""
        game = self.game_simulator.simulate_game(away_team, home_team)
        winner = game.get_winner()
        
        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_score": game.home_team.score,
            "away_score": game.away_team.score,
            "winner": winner.code if winner else home_team,
            "overtime": game.period.value > 3
        }
    
    def simulate_series(self, series: PlayoffSeries) -> PlayoffSeries:
        """
        Simulate an entire best-of-7 series.
        
        Args:
            series: PlayoffSeries to simulate
            
        Returns:
            Completed PlayoffSeries with all game results
        """
        if self.verbose:
            print(f"\nSimulating: {series.higher_seed} vs {series.lower_seed} (Round {series.round.value})")
        
        while not series.is_complete:
            # Determine home team for next game
            home_team = series.get_next_home_team()
            away_team = series.lower_seed if home_team == series.higher_seed else series.higher_seed
            
            # Simulate game
            result = self.simulate_game(home_team, away_team)
            
            # Add result to series
            series.add_game_result(
                winner=result['winner'],
                home_score=result['home_score'],
                away_score=result['away_score'],
                home_team=result['home_team'],
                away_team=result['away_team'],
                overtime=result['overtime']
            )
            
            if self.verbose:
                ot_str = " (OT)" if result['overtime'] else ""
                print(f"  Game {series.games_played}: {result['home_team']} {result['home_score']}, "
                      f"{result['away_team']} {result['away_score']}{ot_str} - "
                      f"Series: {series.higher_seed} {series.higher_seed_wins}-{series.lower_seed_wins} {series.lower_seed}")
        
        if self.verbose:
            print(f"  ✓ {series.winner} wins series {series.higher_seed_wins if series.winner == series.higher_seed else series.lower_seed_wins}-"
                  f"{series.lower_seed_wins if series.winner == series.higher_seed else series.higher_seed_wins}")
        
        return series
    
    def simulate_round(self, round_num: Round) -> bool:
        """
        Simulate all series in a specific round.
        
        Returns:
            True if round completed successfully, False if no series to simulate
        """
        if not self.bracket:
            raise ValueError("No bracket generated. Call generate_bracket() first.")
        
        # Get series for this round
        round_series = [s for s in self.bracket.get_all_series() if s.round == round_num and s.status != SeriesStatus.COMPLETED]
        
        if not round_series:
            return False
        
        if self.verbose:
            round_names = {1: "FIRST ROUND", 2: "SECOND ROUND", 3: "CONFERENCE FINALS", 4: "STANLEY CUP FINALS"}
            print(f"\n{'='*80}")
            print(f"{round_names[round_num.value]}")
            print(f"{'='*80}")
        
        # Simulate all series in this round
        for series in round_series:
            self.simulate_series(series)
        
        # Advance winners to next round
        self._advance_winners(round_num)
        
        return True
    
    def _advance_winners(self, completed_round: Round):
        """Advance series winners to the next round."""
        if completed_round == Round.FIRST_ROUND:
            # Advance to Second Round
            eastern_winners = [s.winner for s in self.bracket.eastern_conference[:4] if s.winner]
            western_winners = [s.winner for s in self.bracket.western_conference[:4] if s.winner]
            
            if len(eastern_winners) == 4:
                self.bracket.eastern_conference.extend([
                    self._create_series("E-R2-1", Round.SECOND_ROUND, eastern_winners[0], eastern_winners[3]),
                    self._create_series("E-R2-2", Round.SECOND_ROUND, eastern_winners[1], eastern_winners[2]),
                ])
            
            if len(western_winners) == 4:
                self.bracket.western_conference.extend([
                    self._create_series("W-R2-1", Round.SECOND_ROUND, western_winners[0], western_winners[3]),
                    self._create_series("W-R2-2", Round.SECOND_ROUND, western_winners[1], western_winners[2]),
                ])
        
        elif completed_round == Round.SECOND_ROUND:
            # Advance to Conference Finals
            eastern_winners = [s.winner for s in self.bracket.eastern_conference[4:6] if s.winner]
            western_winners = [s.winner for s in self.bracket.western_conference[4:6] if s.winner]
            
            if len(eastern_winners) == 2:
                self.bracket.eastern_conference.append(
                    self._create_series("E-CF", Round.CONFERENCE_FINALS, eastern_winners[0], eastern_winners[1])
                )
            
            if len(western_winners) == 2:
                self.bracket.western_conference.append(
                    self._create_series("W-CF", Round.CONFERENCE_FINALS, western_winners[0], western_winners[1])
                )
        
        elif completed_round == Round.CONFERENCE_FINALS:
            # Advance to Stanley Cup Finals
            eastern_champ = self.bracket.eastern_conference[-1].winner if len(self.bracket.eastern_conference) >= 7 else None
            western_champ = self.bracket.western_conference[-1].winner if len(self.bracket.western_conference) >= 7 else None
            
            if eastern_champ and western_champ:
                self.bracket.stanley_cup_finals = self._create_series(
                    "SCF", Round.STANLEY_CUP_FINALS, eastern_champ, western_champ
                )
        
        elif completed_round == Round.STANLEY_CUP_FINALS:
            # Set champion
            if self.bracket.stanley_cup_finals and self.bracket.stanley_cup_finals.winner:
                self.bracket.champion = self.bracket.stanley_cup_finals.winner
                if self.verbose:
                    print(f"\n🏆 STANLEY CUP CHAMPION: {self.bracket.champion} 🏆\n")
    
    def simulate_playoffs(self) -> PlayoffBracket:
        """Simulate entire playoffs from start to finish."""
        if not self.bracket:
            raise ValueError("No bracket generated. Call generate_bracket() first.")
        
        # Simulate all four rounds
        for round_num in [Round.FIRST_ROUND, Round.SECOND_ROUND, Round.CONFERENCE_FINALS, Round.STANLEY_CUP_FINALS]:
            self.simulate_round(round_num)
        
        return self.bracket


