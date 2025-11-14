"""
NHL Game Simulator

Simulates hockey games with AI-driven decision making via the Intelligence Service.
Supports real NHL team data for enhanced realism.
"""

import random
import time
from typing import Dict, Optional, Callable, Union, List, Tuple
import httpx

from game_state import (
    GameState, TeamState, EventType, GamePeriod, 
    StrengthSituation, GameEvent
)
from nhl_data import NHLTeam, get_team, Player


class NHLSimulator:
    """
    NHL Game Simulator with intelligent AI decision making.
    
    Queries the Intelligence Service API for strategic decisions,
    creating a "living game" that improves as the ML model improves.
    
    Now supports real NHL team data for enhanced realism!
    """
    
    def __init__(
        self, 
        api_url: str = "http://localhost:8000",
        verbose: bool = True,
        event_callback: Optional[Callable] = None,
        home_ice_advantage: float = 1.10
    ):
        """
        Initialize simulator.
        
        Args:
            api_url: URL of the Intelligence Service API
            verbose: Print events to console
            event_callback: Optional callback function for events
            home_ice_advantage: Multiplier for home team (default 1.10 = 10% boost)
        """
        self.api_url = api_url
        self.verbose = verbose
        self.event_callback = event_callback
        self.home_ice_advantage = home_ice_advantage
        self.client = httpx.Client(timeout=10.0)
        
        # Track real team data if available
        self.home_nhl_team: Optional[NHLTeam] = None
        self.away_nhl_team: Optional[NHLTeam] = None
        
        # Store ML predictions for this game
        self.ml_prediction: Optional[Dict] = None
    
    def _select_shooter(self, team: NHLTeam, is_power_play: bool = False) -> Optional[Player]:
        """
        Select a player to take a shot, weighted by offensive ability.
        
        Args:
            team: NHL team
            is_power_play: If True, bias toward top players
            
        Returns:
            Selected player or None if no team data
        """
        if not team or not team.roster:
            return None
        
        # Get all forwards and defensemen
        forwards = team.roster.centers + team.roster.left_wings + team.roster.right_wings
        defensemen = team.roster.defensemen
        
        if not forwards and not defensemen:
            return None
        
        # On power play or generally, forwards shoot 75% of the time
        shoot_from_forwards = random.random() < 0.75
        
        if shoot_from_forwards and forwards:
            players = forwards
        elif defensemen:
            players = defensemen
        else:
            players = forwards
        
        # Weight by offensive rating and shots_per_60
        # Higher rating = higher chance to shoot
        weights = []
        for player in players:
            # Base weight on rating (0-100)
            weight = player.rating
            
            # Bonus for shot-takers
            if player.shots_per_60 > 0:
                weight += player.shots_per_60 * 5  # Multiply by 5 to boost high-volume shooters
            
            # On PP, heavily favor top players
            if is_power_play:
                weight = weight * 1.5 if player.rating > 80 else weight * 0.7
            
            weights.append(max(weight, 10))  # Minimum weight of 10
        
        return random.choices(players, weights=weights)[0]
    
    def _select_assists(
        self, 
        team: NHLTeam, 
        scorer: Optional[Player]
    ) -> Tuple[Optional[Player], Optional[Player]]:
        """
        Select players for primary and secondary assists.
        
        Args:
            team: NHL team
            scorer: Player who scored (to exclude from assists)
            
        Returns:
            Tuple of (primary_assist, secondary_assist)
        """
        if not team or not team.roster:
            return (None, None)
        
        # Get all skaters except the scorer
        all_skaters = (
            team.roster.centers + 
            team.roster.left_wings + 
            team.roster.right_wings + 
            team.roster.defensemen
        )
        
        if scorer:
            all_skaters = [p for p in all_skaters if p.id != scorer.id]
        
        if not all_skaters:
            return (None, None)
        
        # 70% chance of assist
        if random.random() > 0.70:
            return (None, None)
        
        # Weight by playmaking ability (assists_per_60 and rating)
        weights = []
        for player in all_skaters:
            weight = player.rating
            if player.assists_per_60 > 0:
                weight += player.assists_per_60 * 8  # Playmakers get bonus
            weights.append(max(weight, 10))
        
        # Select primary assist
        primary = random.choices(all_skaters, weights=weights)[0]
        
        # 60% chance of secondary assist
        if random.random() > 0.60:
            return (primary, None)
        
        # Remove primary from pool
        remaining = [p for p in all_skaters if p.id != primary.id]
        if not remaining:
            return (primary, None)
        
        # Recalculate weights for remaining players
        secondary_weights = []
        for player in remaining:
            weight = player.rating
            if player.assists_per_60 > 0:
                weight += player.assists_per_60 * 8
            secondary_weights.append(max(weight, 10))
        
        secondary = random.choices(remaining, weights=secondary_weights)[0]
        
        return (primary, secondary)
    
    def _get_starting_goalie(self, team: NHLTeam) -> Optional[Player]:
        """Get the starting goalie for a team."""
        if not team or not team.roster:
            return None
        return team.roster.get_starting_goalie()
    
    def _select_shot_type(self) -> str:
        """Randomly select a shot type."""
        shot_types = {
            "wrist": 0.40,
            "slap": 0.15,
            "snap": 0.25,
            "backhand": 0.10,
            "tip": 0.07,
            "deflection": 0.03
        }
        return random.choices(
            list(shot_types.keys()),
            weights=list(shot_types.values())
        )[0]
    
    def simulate_game(
        self, 
        home_team_code: str,
        home_team_name: Optional[str] = None,
        away_team_code: Optional[str] = None,
        away_team_name: Optional[str] = None
    ) -> GameState:
        """
        Simulate a complete game.
        
        Args:
            home_team_code: Home team abbreviation (e.g., "TOR")
            home_team_name: Home team full name (optional if using NHL data)
            away_team_code: Away team abbreviation (optional for backwards compat)
            away_team_name: Away team full name (optional if using NHL data)
            
        Returns:
            Final game state
        """
        # Support new simple API: simulate_game("MTL", "TOR")
        if away_team_code is None and home_team_name is not None and '@' not in home_team_name:
            # User called: simulate_game("MTL", "TOR")
            away_team_code = home_team_code
            home_team_code = home_team_name
            home_team_name = None
            away_team_name = None
        
        # Try to load NHL team data
        self.home_nhl_team = get_team(home_team_code)
        if away_team_code:
            self.away_nhl_team = get_team(away_team_code)
        
        # Use NHL data names if available
        if self.home_nhl_team and not home_team_name:
            home_team_name = self.home_nhl_team.full_name
        elif not home_team_name:
            home_team_name = home_team_code
            
        if self.away_nhl_team and not away_team_name:
            away_team_name = self.away_nhl_team.full_name
        elif not away_team_name:
            away_team_name = away_team_code
        
        # Query ML model for pre-game prediction
        self.ml_prediction = self._get_pregame_prediction()
        
        # Initialize game
        game_id = f"{away_team_code}@{home_team_code}-{int(time.time())}"
        game = GameState(
            game_id=game_id,
            home_team=TeamState(code=home_team_code, name=home_team_name),
            away_team=TeamState(code=away_team_code, name=away_team_name)
        )
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"SIMULATING: {away_team_name} @ {home_team_name}")
            if self.home_nhl_team and self.away_nhl_team:
                print(f"Home Strength: {self.home_nhl_team.overall_strength:.1f}/100")
                print(f"Away Strength: {self.away_nhl_team.overall_strength:.1f}/100")
                print(f"Home Ice Advantage: {(self.home_ice_advantage - 1) * 100:.0f}%")
            
            # Show ML predictions
            if self.ml_prediction:
                print(f"\n🤖 ML PREDICTION:")
                print(f"   Home Win: {self.ml_prediction['home_win_prob']*100:.1f}%")
                print(f"   Expected Score: {self.ml_prediction['expected_goals_home']:.1f} - {self.ml_prediction['expected_goals_away']:.1f}")
                print(f"   Confidence: {self.ml_prediction['confidence']*100:.0f}%")
            
            print(f"{'='*70}\n")
        
        # Simulate each period
        while not game.is_game_over():
            self._simulate_period(game)
            
            if game.time_remaining == 0 and not game.is_game_over():
                game_continues = game.advance_period()
                if not game_continues:
                    break
        
        # Print final summary
        if self.verbose:
            self._print_final_summary(game)
        
        return game
    
    def _simulate_period(self, game: GameState):
        """Simulate a single period."""
        if self.verbose:
            print(f"\n--- Period {game.period.value} ---\n")
        
        # Special handling for shootout
        if game.period == GamePeriod.SHOOTOUT:
            self._simulate_shootout(game)
            return
        
        while game.time_remaining > 0:
            # Simulate time passage (10-60 seconds per "play")
            time_delta = random.randint(10, 60)
            game.advance_time(time_delta)
            
            # Check for AI decision points
            self._check_ai_decisions(game)
            
            # Generate random event
            self._generate_event(game)
            
            # Small delay for readability (optional)
            if self.verbose:
                time.sleep(0.05)
    
    def _generate_event(self, game: GameState):
        """Generate a random game event based on probabilities."""
        # Event probabilities (adjusted based on situation)
        event_weights = {
            'shot': 0.35,
            'faceoff': 0.20,
            'hit': 0.15,
            'blocked_shot': 0.10,
            'penalty': 0.03,
            'nothing': 0.17
        }
        
        # Adjust for strength situation
        if game.strength_situation != StrengthSituation.EVEN:
            event_weights['shot'] += 0.10  # More shots on power play
            event_weights['penalty'] = 0.01  # Fewer penalties
        
        # Choose event
        event_type = random.choices(
            list(event_weights.keys()),
            weights=list(event_weights.values())
        )[0]
        
        # Determine which team
        # Calculate home advantage based on team strength and home ice
        home_prob = self._calculate_event_probability(is_home=True)
        is_home_event = random.random() < home_prob
        team = game.home_team if is_home_event else game.away_team
        opponent = game.away_team if is_home_event else game.home_team
        
        # Process event
        if event_type == 'shot':
            self._process_shot(game, team, opponent)
        elif event_type == 'faceoff':
            self._process_faceoff(game, team, opponent)
        elif event_type == 'hit':
            self._process_hit(game, team)
        elif event_type == 'blocked_shot':
            self._process_blocked_shot(game, team, opponent)
        elif event_type == 'penalty':
            self._process_penalty(game, team)
    
    def _get_pregame_prediction(self) -> Optional[Dict]:
        """
        Query ML model for pre-game prediction.
        Uses team stats to get expected outcome.
        """
        if not self.home_nhl_team or not self.away_nhl_team:
            return None
        
        try:
            # Prepare request payload
            payload = {
                "home_team_id": self.home_nhl_team.code,
                "away_team_id": self.away_nhl_team.code,
                "period": 1,
                "time_remaining": 60.0,
                "score_home": 0,
                "score_away": 0,
                "home_stats": {
                    "goals_per_game": self.home_nhl_team.stats.goals_per_game,
                    "goals_against_per_game": self.home_nhl_team.stats.goals_against_per_game,
                    "xGF_pct": self.home_nhl_team.stats.xGF_pct,
                    "corsi_for_pct": self.home_nhl_team.stats.corsi_for_pct,
                },
                "away_stats": {
                    "goals_per_game": self.away_nhl_team.stats.goals_per_game,
                    "goals_against_per_game": self.away_nhl_team.stats.goals_against_per_game,
                    "xGF_pct": self.away_nhl_team.stats.xGF_pct,
                    "corsi_for_pct": self.away_nhl_team.stats.corsi_for_pct,
                }
            }
            
            # Query API
            response = self.client.post(
                f"{self.api_url}/predict-game",
                json=payload,
                timeout=5.0
            )
            
            if response.status_code == 200:
                prediction = response.json()
                if self.verbose:
                    print(f"[ML] Pre-game prediction received (confidence: {prediction.get('confidence', 0)*100:.0f}%)")
                return prediction
            else:
                if self.verbose:
                    print(f"[ML] Prediction API returned {response.status_code}, using defaults")
                return None
                
        except Exception as e:
            if self.verbose:
                print(f"[ML] Could not get prediction: {e}")
            return None
    
    def _calculate_event_probability(self, is_home: bool) -> float:
        """
        Calculate probability of home team having possession/event.
        Factors in team strength and home ice advantage.
        """
        if not self.home_nhl_team or not self.away_nhl_team:
            # No team data - use default with home ice
            return 0.50 * self.home_ice_advantage if is_home else 0.50
        
        # Get team strengths (0-100)
        home_strength = self.home_nhl_team.overall_strength
        away_strength = self.away_nhl_team.overall_strength
        
        # Apply home ice advantage
        home_strength *= self.home_ice_advantage
        
        # Calculate probability (normalize to 0-1)
        total = home_strength + away_strength
        home_prob = home_strength / total
        
        return home_prob if is_home else (1 - home_prob)
    
    def _calculate_goal_probability_modifier(self, shooting_team: TeamState, defending_team: TeamState) -> float:
        """
        Calculate goal probability modifier based on team strengths.
        Returns a multiplier (1.0 = average, >1.0 = better offense/worse defense).
        """
        modifier = 1.0
        
        # Check if we have NHL team data
        is_home_shooting = (shooting_team.code == self.home_nhl_team.code if self.home_nhl_team else True)
        
        if is_home_shooting and self.home_nhl_team:
            shooting_nhl = self.home_nhl_team
            defending_nhl = self.away_nhl_team
        elif not is_home_shooting and self.away_nhl_team:
            shooting_nhl = self.away_nhl_team
            defending_nhl = self.home_nhl_team
        else:
            return modifier  # No data, use default
        
        if shooting_nhl and defending_nhl:
            # Offensive strength (0-100) -> convert to multiplier (0.7-1.3)
            off_modifier = 0.7 + (shooting_nhl.offensive_strength / 100) * 0.6
            
            # Defensive strength (0-100) -> INVERSE for goals against (0.7-1.3)
            # Higher defense = lower modifier for opponent scoring
            def_modifier = 1.3 - (defending_nhl.defensive_strength / 100) * 0.6
            
            modifier = off_modifier * def_modifier
        
        return modifier
    
    def _calculate_ml_guided_goal_probability(self, shooting_team: TeamState, defending_team: TeamState) -> float:
        """
        Calculate goal probability guided by ML predictions.
        This is the KEY innovation - simulation conforms to ML model expectations.
        """
        # If we have ML predictions, use them to set realistic probabilities
        if self.ml_prediction:
            # Determine which team is shooting
            is_home_shooting = (shooting_team.code == self.home_nhl_team.code if self.home_nhl_team else True)
            
            # Get expected goals for this team
            if is_home_shooting:
                expected_goals = self.ml_prediction['expected_goals_home']
            else:
                expected_goals = self.ml_prediction['expected_goals_away']
            
            # Expected shots per game (roughly 30 per team)
            expected_shots = 30.0
            
            # Calculate target conversion rate: expected_goals / expected_shots
            # This ensures simulation output matches ML prediction
            target_conversion = expected_goals / expected_shots
            
            # The actual probability per shot to hit ML target
            # Add 20% buffer for realism variance
            goal_prob = target_conversion * 1.1  # Slightly higher to account for missed shots
            
            return float(max(0.05, min(0.25, goal_prob)))  # Clip between 5-25%
        
        # Fallback to team strength if no ML prediction
        base_goal_prob = 0.12  # Increased from 0.10 for more scoring
        strength_modifier = self._calculate_goal_probability_modifier(shooting_team, defending_team)
        return base_goal_prob * strength_modifier
    
    def _process_shot(self, game: GameState, shooting_team: TeamState, defending_team: TeamState):
        """Process a shot on goal with player attribution."""
        shooting_team.shots += 1
        shooting_team.shot_attempts += 1
        shooting_team.corsi_for += 1
        defending_team.corsi_against += 1
        
        # Determine which NHL team is shooting
        is_home_shooting = (shooting_team.code == self.home_nhl_team.code if self.home_nhl_team else True)
        shooting_nhl_team = self.home_nhl_team if is_home_shooting else self.away_nhl_team
        defending_nhl_team = self.away_nhl_team if is_home_shooting else self.home_nhl_team
        
        # Select shooter and goalie
        is_pp = game.strength_situation in [StrengthSituation.PP_MAJOR, StrengthSituation.PP_MINOR]
        shooter = self._select_shooter(shooting_nhl_team, is_power_play=is_pp) if shooting_nhl_team else None
        goalie = self._get_starting_goalie(defending_nhl_team) if defending_nhl_team else None
        shot_type = self._select_shot_type()
        
        # Goal probability - use ML prediction if available
        base_goal_prob = self._calculate_ml_guided_goal_probability(shooting_team, defending_team)
        
        # Adjust for power play
        if game.strength_situation == StrengthSituation.PP_MAJOR:
            if game.active_penalties[0]['team'] != shooting_team.code:
                base_goal_prob *= 1.8  # 80% boost on power play
        
        # Adjust for empty net
        is_empty_net = defending_team.goalie_pulled
        if is_empty_net:
            base_goal_prob = 0.35  # 35% on empty net (overrides other factors)
        
        # Check if goal
        if random.random() < base_goal_prob:
            # GOAL! Select assists
            primary_assist = None
            secondary_assist = None
            
            if shooting_nhl_team:
                primary, secondary = self._select_assists(shooting_nhl_team, shooter)
                primary_assist = primary
                secondary_assist = secondary
            
            # Record goal with full attribution
            game.score_goal(
                shooting_team.code, 
                is_power_play=is_pp,
                scorer_name=shooter.name if shooter else None,
                scorer_id=shooter.id if shooter else None,
                primary_assist=primary_assist.name if primary_assist else None,
                primary_assist_id=primary_assist.id if primary_assist else None,
                secondary_assist=secondary_assist.name if secondary_assist else None,
                secondary_assist_id=secondary_assist.id if secondary_assist else None,
                is_empty_net=is_empty_net,
                shot_type=shot_type
            )
            
            # Update xG
            shooting_team.expected_goals += base_goal_prob
            
            if self.verbose:
                mins = game.time_remaining // 60
                secs = game.time_remaining % 60
                goal_desc = f"[{game.period.value}P {mins:02d}:{secs:02d}] GOAL! "
                if shooter:
                    goal_desc += f"{shooter.name}"
                    if primary_assist or secondary_assist:
                        assists = []
                        if primary_assist:
                            assists.append(primary_assist.name)
                        if secondary_assist:
                            assists.append(secondary_assist.name)
                        goal_desc += f" ({', '.join(assists)})"
                else:
                    goal_desc += f"{shooting_team.name}"
                goal_desc += f"! ({game.home_team.score}-{game.away_team.score})"
                if is_pp:
                    goal_desc += " - PP"
                if is_empty_net:
                    goal_desc += " - EN"
                print(goal_desc)
            
            if self.event_callback:
                self.event_callback(game.events[-1])
        else:
            # Save
            if self.verbose and random.random() < 0.15:  # Only print 15% of saves
                mins = game.time_remaining // 60
                secs = game.time_remaining % 60
                save_desc = f"[{game.period.value}P {mins:02d}:{secs:02d}] "
                if goalie:
                    save_desc += f"Save by {goalie.name}"
                else:
                    save_desc += f"Save by {defending_team.name}"
                print(save_desc)
    
    def _process_faceoff(self, game: GameState, team: TeamState, opponent: TeamState):
        """Process a faceoff."""
        if random.random() < 0.5:
            team.faceoffs_won += 1
            opponent.faceoffs_lost += 1
        else:
            team.faceoffs_lost += 1
            opponent.faceoffs_won += 1
    
    def _process_hit(self, game: GameState, team: TeamState):
        """Process a hit."""
        team.hits += 1
        
        if self.verbose and random.random() < 0.1:  # Print 10% of hits
            mins = game.time_remaining // 60
            secs = game.time_remaining % 60
            print(f"[{game.period.value}P {mins:02d}:{secs:02d}] Big hit by {team.name}!")
    
    def _process_blocked_shot(self, game: GameState, blocking_team: TeamState, shooting_team: TeamState):
        """Process a blocked shot."""
        blocking_team.blocked_shots += 1
        shooting_team.shot_attempts += 1
        shooting_team.corsi_for += 1
        blocking_team.corsi_against += 1
    
    def _process_penalty(self, game: GameState, team: TeamState):
        """Process a penalty."""
        penalties = [
            ("Tripping", 2),
            ("Hooking", 2),
            ("Slashing", 2),
            ("High-sticking", 2),
            ("Interference", 2),
            ("Roughing", 2),
            ("Cross-checking", 2),
            ("Holding", 2),
        ]
        
        penalty_name, minutes = random.choice(penalties)
        game.add_penalty(team.code, minutes, f"{penalty_name} - {minutes} minutes")
        
        opponent = game.away_team if team == game.home_team else game.home_team
        opponent.power_play_opportunities += 1
        
        if self.verbose:
            mins = game.time_remaining // 60
            secs = game.time_remaining % 60
            print(f"[{game.period.value}P {mins:02d}:{secs:02d}] PENALTY: {team.name} - {penalty_name} ({minutes} min)")
    
    def _check_ai_decisions(self, game: GameState):
        """Check if AI should make any strategic decisions."""
        # Only check during critical moments
        if game.time_remaining > 300:  # More than 5 minutes left
            return
        
        # Check goalie pull decision (trailing team in late game)
        self._check_goalie_pull(game)
    
    def _check_goalie_pull(self, game: GameState):
        """Query Intelligence Service for goalie pull decision."""
        # Only for regulation or OT
        if game.period not in [GamePeriod.THIRD, GamePeriod.OVERTIME]:
            return
        
        # Check if home team should pull goalie
        if game.home_team.score < game.away_team.score and not game.home_team.goalie_pulled:
            if self._should_pull_goalie(game, game.home_team, game.away_team):
                game.home_team.goalie_pulled = True
                game.add_event(EventType.GOALIE_PULL, game.home_team.code, f"{game.home_team.name} pulls goalie")
                if self.verbose:
                    mins = game.time_remaining // 60
                    secs = game.time_remaining % 60
                    print(f"\n[{game.period.value}P {mins:02d}:{secs:02d}] ** AI DECISION: {game.home_team.name} pulls goalie! **\n")
        
        # Check if away team should pull goalie
        if game.away_team.score < game.home_team.score and not game.away_team.goalie_pulled:
            if self._should_pull_goalie(game, game.away_team, game.home_team):
                game.away_team.goalie_pulled = True
                game.add_event(EventType.GOALIE_PULL, game.away_team.code, f"{game.away_team.name} pulls goalie")
                if self.verbose:
                    mins = game.time_remaining // 60
                    secs = game.time_remaining % 60
                    print(f"\n[{game.period.value}P {mins:02d}:{secs:02d}] ** AI DECISION: {game.away_team.name} pulls goalie! **\n")
    
    def _should_pull_goalie(self, game: GameState, trailing_team: TeamState, leading_team: TeamState) -> bool:
        """
        Query Intelligence Service to decide if goalie should be pulled.
        
        This is where the "living game" magic happens!
        """
        try:
            response = self.client.post(
                f"{self.api_url}/recommend-decision",
                json={
                    "game_state": game.to_dict(),
                    "decision_type": "pull_goalie",
                    "context": {
                        "score_diff": trailing_team.score - leading_team.score,
                        "time_remaining": game.time_remaining,
                        "period": game.period.value
                    }
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                should_pull = data.get('recommendation') == 'pull_goalie'
                confidence = data.get('confidence', 0)
                
                # Only pull if AI is confident
                return should_pull and confidence > 0.5
            
        except Exception as e:
            # Fallback to simple rule if API fails
            if self.verbose:
                print(f"[AI] API unavailable, using fallback logic: {e}")
            pass
        
        # Fallback logic: pull goalie if down 1 with < 2 min left, or down 2+ with < 3 min
        score_diff = abs(trailing_team.score - leading_team.score)
        if score_diff == 1 and game.time_remaining < 120:
            return True
        if score_diff >= 2 and game.time_remaining < 180:
            return True
        
        return False
    
    def _simulate_shootout(self, game: GameState):
        """Simulate a shootout."""
        if self.verbose:
            print("\n--- SHOOTOUT ---\n")
        
        home_goals = 0
        away_goals = 0
        
        # 3 rounds minimum
        for round_num in range(1, 4):
            # Away team shoots first
            if random.random() < 0.33:  # 33% shootout goal rate
                away_goals += 1
                if self.verbose:
                    print(f"Round {round_num}: {game.away_team.name} SCORES!")
            else:
                if self.verbose:
                    print(f"Round {round_num}: {game.away_team.name} - Save")
            
            # Home team shoots
            if random.random() < 0.33:
                home_goals += 1
                if self.verbose:
                    print(f"Round {round_num}: {game.home_team.name} SCORES!")
            else:
                if self.verbose:
                    print(f"Round {round_num}: {game.home_team.name} - Save")
        
        # Sudden death if tied after 3
        round_num = 4
        while home_goals == away_goals:
            if random.random() < 0.33:
                away_goals += 1
                if self.verbose:
                    print(f"Round {round_num}: {game.away_team.name} SCORES!")
            
            if home_goals == away_goals:  # Still tied, home shoots
                if random.random() < 0.33:
                    home_goals += 1
                    if self.verbose:
                        print(f"Round {round_num}: {game.home_team.name} SCORES!")
            
            round_num += 1
        
        # Award goal to winner
        if home_goals > away_goals:
            game.home_team.score += 1
        else:
            game.away_team.score += 1
        
        game._end_game()
    
    def _print_final_summary(self, game: GameState):
        """Print final game summary."""
        winner = game.get_winner()
        
        print(f"\n{'='*70}")
        print(f"FINAL SCORE")
        print(f"{'='*70}")
        print(f"{game.away_team.name}: {game.away_team.score}")
        print(f"{game.home_team.name}: {game.home_team.score}")
        print(f"\nWinner: {winner.name}")
        print(f"{'='*70}\n")
        
        # Stats
        print("GAME STATS")
        print(f"{'='*70}")
        print(f"{'Stat':<25} {game.away_team.code:>10} {game.home_team.code:>10}")
        print(f"{'-'*70}")
        print(f"{'Shots':<25} {game.away_team.shots:>10} {game.home_team.shots:>10}")
        print(f"{'Shot Attempts':<25} {game.away_team.shot_attempts:>10} {game.home_team.shot_attempts:>10}")
        print(f"{'Hits':<25} {game.away_team.hits:>10} {game.home_team.hits:>10}")
        print(f"{'Blocked Shots':<25} {game.away_team.blocked_shots:>10} {game.home_team.blocked_shots:>10}")
        print(f"{'Faceoff Wins':<25} {game.away_team.faceoffs_won:>10} {game.home_team.faceoffs_won:>10}")
        print(f"{'Penalties':<25} {game.away_team.penalties:>10} {game.home_team.penalties:>10}")
        print(f"{'PP Goals/Opps':<25} {game.away_team.power_play_goals}/{game.away_team.power_play_opportunities:>9} {game.home_team.power_play_goals}/{game.home_team.power_play_opportunities:>9}")
        print(f"{'Expected Goals':<25} {game.away_team.expected_goals:>10.2f} {game.home_team.expected_goals:>10.2f}")
        print(f"{'='*70}\n")
        
        print(f"Total Events: {len(game.events)}")
        print(f"Game Duration: {game.period.value} period(s)")
        print()

