"""
NHL Season Simulator

Simulates complete 82-game NHL seasons with standings and playoffs.
"""

import sys
import io
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random

if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from simulator import NHLSimulator
from nhl_loader import load_all_teams
from nhl_data import NHL_TEAMS, NHLTeam
from game_state import GameState
from player_stats_tracker import PlayerStatsTracker


@dataclass
class TeamRecord:
    """Season record for a team."""
    team_code: str
    team_name: str
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    otl: int = 0  # Overtime/shootout losses
    goals_for: int = 0
    goals_against: int = 0
    
    @property
    def points(self) -> int:
        """Calculate points (W=2, OTL=1)."""
        return self.wins * 2 + self.otl
    
    @property
    def goal_differential(self) -> int:
        """Goal differential."""
        return self.goals_for - self.goals_against
    
    @property
    def points_percentage(self) -> float:
        """Points percentage."""
        max_points = self.games_played * 2
        return (self.points / max_points * 100) if max_points > 0 else 0.0


@dataclass
class Game:
    """A scheduled game."""
    home_team: str
    away_team: str
    date: datetime
    played: bool = False
    home_score: int = 0
    away_score: int = 0
    overtime: bool = False


class SeasonSimulator:
    """
    Simulates complete NHL seasons.
    """
    
    def __init__(self, season_year: str = "2024-25", verbose: bool = True):
        """
        Initialize season simulator.
        
        Args:
            season_year: Season year (e.g., "2024-25")
            verbose: Print progress
        """
        self.season_year = season_year
        self.verbose = verbose
        self.simulator = NHLSimulator(verbose=False)
        
        # Load teams
        if not NHL_TEAMS:
            load_all_teams()
        
        # Initialize records
        self.records: Dict[str, TeamRecord] = {}
        for code, team in NHL_TEAMS.items():
            self.records[code] = TeamRecord(
                team_code=code,
                team_name=team.full_name
            )
        
        # Initialize player stats tracker
        self.stats_tracker = PlayerStatsTracker(season_year=season_year)
        
        # Generate schedule
        self.schedule: List[Game] = []
        self._generate_schedule()
    
    def _generate_schedule(self):
        """Generate an 82-game season schedule."""
        start_date = datetime(2024, 10, 10)  # Season starts mid-October
        
        teams = list(NHL_TEAMS.keys())
        game_date = start_date
        
        # Simple schedule: each team plays every other team 2-3 times
        # Division rivals play 4 times, others 2-3 times
        # For MVP: simplified to ensure 82 games per team
        
        games_per_matchup = {}
        
        # Division matchups: 4 games
        for team_code, team in NHL_TEAMS.items():
            division_teams = [t for t, tm in NHL_TEAMS.items() 
                            if tm.division == team.division and t != team_code]
            for opp in division_teams:
                key = tuple(sorted([team_code, opp]))
                games_per_matchup[key] = 4
        
        # Conference matchups (non-division): 3 games
        for team_code, team in NHL_TEAMS.items():
            conf_teams = [t for t, tm in NHL_TEAMS.items() 
                         if tm.conference == team.conference 
                         and tm.division != team.division 
                         and t != team_code]
            for opp in conf_teams:
                key = tuple(sorted([team_code, opp]))
                if key not in games_per_matchup:
                    games_per_matchup[key] = 3
        
        # Other conference: 2 games
        for team_code, team in NHL_TEAMS.items():
            other_teams = [t for t, tm in NHL_TEAMS.items() 
                          if tm.conference != team.conference]
            for opp in other_teams:
                key = tuple(sorted([team_code, opp]))
                if key not in games_per_matchup:
                    games_per_matchup[key] = 2
        
        # Create games
        for (team1, team2), num_games in games_per_matchup.items():
            for i in range(num_games):
                # Alternate home/away
                if i % 2 == 0:
                    home, away = team1, team2
                else:
                    home, away = team2, team1
                
                self.schedule.append(Game(
                    home_team=home,
                    away_team=away,
                    date=game_date
                ))
                
                game_date += timedelta(days=1)
        
        # Shuffle for variety
        random.shuffle(self.schedule)
        
        if self.verbose:
            print(f"Generated schedule: {len(self.schedule)} games")
    
    def simulate_season(self, num_games: int = None) -> Dict[str, TeamRecord]:
        """
        Simulate the season.
        
        Args:
            num_games: Number of games to simulate (None = full season)
        
        Returns:
            Dictionary of team records
        """
        games_to_sim = num_games if num_games else len(self.schedule)
        games_to_sim = min(games_to_sim, len(self.schedule))
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"SIMULATING {self.season_year} SEASON")
            print(f"{'='*70}")
            print(f"Games to simulate: {games_to_sim}")
            print()
        
        for i, game in enumerate(self.schedule[:games_to_sim]):
            if game.played:
                continue
            
            # Simulate game
            result = self.simulator.simulate_game(game.away_team, game.home_team)
            
            # Record results
            game.played = True
            game.home_score = result.home_team.score
            game.away_score = result.away_team.score
            game.overtime = result.period.value > 3
            
            # Track player stats from game
            self._track_player_stats_from_game(result)
            
            # Update records
            home_record = self.records[game.home_team]
            away_record = self.records[game.away_team]
            
            home_record.games_played += 1
            away_record.games_played += 1
            home_record.goals_for += game.home_score
            home_record.goals_against += game.away_score
            away_record.goals_for += game.away_score
            away_record.goals_against += game.home_score
            
            if game.home_score > game.away_score:
                # Home win
                home_record.wins += 1
                if game.overtime:
                    away_record.otl += 1
                else:
                    away_record.losses += 1
            else:
                # Away win
                away_record.wins += 1
                if game.overtime:
                    home_record.otl += 1
                else:
                    home_record.losses += 1
            
            # Progress update
            if self.verbose and (i + 1) % 100 == 0:
                print(f"  Simulated {i + 1}/{games_to_sim} games...")
        
        if self.verbose:
            print(f"\n✅ Season simulation complete!")
            self._print_standings()
        
        return self.records
    
    def _track_player_stats_from_game(self, game: GameState):
        """Extract and track player stats from a completed game."""
        # Process all goals from period scores
        for period_num, period_score in game.period_scores.items():
            for goal in period_score.goals:
                scorer_id = goal.get('scorer_id')
                scorer_name = goal.get('scorer')
                team_code = goal.get('team')
                
                if scorer_id and scorer_name and team_code:
                    # Record goal with assists
                    self.stats_tracker.record_goal(
                        scorer_id=scorer_id,
                        scorer_name=scorer_name,
                        team_code=team_code,
                        position="F",  # Default to forward (would need position tracking)
                        primary_assist_id=goal.get('primary_assist_id') if goal.get('primary_assist') else None,
                        primary_assist_name=goal.get('primary_assist'),
                        secondary_assist_id=goal.get('secondary_assist_id') if goal.get('secondary_assist') else None,
                        secondary_assist_name=goal.get('secondary_assist')
                    )
    
    def _print_standings(self):
        """Print current standings."""
        print(f"\n{'='*70}")
        print(f"STANDINGS - {self.season_year} SEASON")
        print(f"{'='*70}\n")
        
        conferences = ["Eastern", "Western"]
        
        for conference in conferences:
            print(f"\n{conference.upper()} CONFERENCE")
            print("-" * 70)
            
            # Get teams in conference
            conf_teams = [code for code, team in NHL_TEAMS.items() 
                         if team.conference == conference]
            
            # Sort by points
            sorted_teams = sorted(
                [self.records[code] for code in conf_teams],
                key=lambda r: (r.points, r.wins, r.goal_differential),
                reverse=True
            )
            
            # Print header
            print(f"{'Rank':<6}{'Team':<30}{'GP':<5}{'W':<4}{'L':<4}{'OTL':<5}{'PTS':<5}{'GF':<5}{'GA':<5}{'DIFF':<6}{'P%':<6}")
            print("-" * 70)
            
            # Print teams
            for i, record in enumerate(sorted_teams, 1):
                playoff_marker = "*" if i <= 8 else " "
                print(f"{playoff_marker}{i:<5}{record.team_name:<30}{record.games_played:<5}"
                      f"{record.wins:<4}{record.losses:<4}{record.otl:<5}{record.points:<5}"
                      f"{record.goals_for:<5}{record.goals_against:<5}{record.goal_differential:<+6}"
                      f"{record.points_percentage:<6.1f}")
    
    def get_playoff_teams(self) -> Dict[str, List[TeamRecord]]:
        """Get top 8 teams from each conference."""
        playoffs = {}
        
        for conference in ["Eastern", "Western"]:
            conf_teams = [code for code, team in NHL_TEAMS.items() 
                         if team.conference == conference]
            
            sorted_teams = sorted(
                [self.records[code] for code in conf_teams],
                key=lambda r: (r.points, r.wins, r.goal_differential),
                reverse=True
            )
            
            playoffs[conference] = sorted_teams[:8]
        
        return playoffs


if __name__ == "__main__":
    """Test season simulator."""
    
    print("NHL Season Simulator Test")
    print("="*70)
    print()
    
    # Simulate first 20 games of season
    season = SeasonSimulator(season_year="2024-25", verbose=True)
    records = season.simulate_season(num_games=20)
    
    print("\n" + "="*70)
    print("EARLY SEASON LEADERS")
    print("="*70)
    
    # Top 5 teams
    all_teams = sorted(records.values(), 
                      key=lambda r: (r.points, r.goal_differential), 
                      reverse=True)
    
    print("\nTop 5 Teams:")
    for i, record in enumerate(all_teams[:5], 1):
        print(f"{i}. {record.team_name}: {record.wins}-{record.losses}-{record.otl} ({record.points} pts)")


