"""
Puckcast Model Client

This module connects to the Puckcast prediction model WITHOUT modifying it.
It acts as a bridge between the game and the ML model.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np

# Add puckcast to path (adjust path as needed)
# Puckcast is in C:\Users\rhine\New folder (2)\puckcast
PUCKCAST_PATH = Path(r'C:\Users\rhine\New folder (2)\puckcast')
if not PUCKCAST_PATH.exists():
    raise RuntimeError(f"Puckcast not found at {PUCKCAST_PATH}")
sys.path.insert(0, str(PUCKCAST_PATH / 'src'))

from nhl_prediction.pipeline import build_dataset, Dataset
from nhl_prediction.model import create_baseline_model, fit_model, predict_probabilities


class PuckcastClient:
    """
    Client for interacting with Puckcast prediction model.
    
    This class loads the Puckcast model and provides a clean interface
    for the game to query predictions without modifying the original model.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize Puckcast client.
        
        Args:
            model_path: Optional path to saved model. If None, trains new model.
        """
        self.model_path = model_path
        self.model = None
        self.dataset = None
        self.version = "1.0.0"
        
        # Load or train model
        self._initialize_model()
    
    def _initialize_model(self):
        """Load or train the prediction model."""
        print("Loading Puckcast model...")
        
        try:
            # Build dataset (using existing seasons)
            self.dataset = build_dataset(['20212022', '20222023', '20232024'])
            
            # Train model
            train_mask = self.dataset.games['seasonId'].isin(['20212022', '20222023', '20232024'])
            self.model = create_baseline_model(C=1.0)
            self.model = fit_model(self.model, self.dataset.features, self.dataset.target, train_mask)
            
            print("[OK] Puckcast model loaded successfully")
            
        except Exception as e:
            print(f"[ERROR] Error loading model: {e}")
            raise
    
    def predict_game_outcome(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict outcome of a game given current state.
        
        Args:
            game_state: Dictionary containing:
                - home_team_id: int or str (team code)
                - away_team_id: int or str (team code)
                - period: int (1-3)
                - time_remaining: float (minutes)
                - score_home: int
                - score_away: int
                - home_stats: dict (optional - team season stats)
                - away_stats: dict (optional - team season stats)
        
        Returns:
            Dictionary with:
                - home_win_prob: float (0-1)
                - away_win_prob: float (0-1)
                - expected_goals_home: float
                - expected_goals_away: float
                - confidence: float (0-1)
                - model_version: str
        """
        try:
            # Use team stats if provided (preferred)
            if 'home_stats' in game_state and 'away_stats' in game_state:
                return self._predict_from_team_stats(game_state)
            
            # Otherwise use simpler in-game prediction
            home_win_prob = self._simple_prediction(game_state)
            
            return {
                'home_win_prob': float(home_win_prob),
                'away_win_prob': float(1 - home_win_prob),
                'expected_goals_home': float(game_state.get('score_home', 0) + (60 - game_state.get('time_remaining', 0)) / 20),
                'expected_goals_away': float(game_state.get('score_away', 0) + (60 - game_state.get('time_remaining', 0)) / 20),
                'confidence': 0.75,
                'model_version': self.version
            }
            
        except Exception as e:
            print(f"Error predicting game: {e}")
            # Return default prediction
            return {
                'home_win_prob': 0.55,
                'away_win_prob': 0.45,
                'expected_goals_home': 2.5,
                'expected_goals_away': 2.3,
                'confidence': 0.5,
                'model_version': self.version,
                'error': str(e)
            }
    
    def _predict_from_team_stats(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict game outcome using team season statistics.
        This creates a realistic pre-game prediction.
        """
        home_stats = game_state['home_stats']
        away_stats = game_state['away_stats']
        
        # Extract key stats
        home_gf = home_stats.get('goals_per_game', 3.0)
        home_ga = home_stats.get('goals_against_per_game', 3.0)
        home_xgf_pct = home_stats.get('xGF_pct', 50.0) / 100.0
        home_corsi = home_stats.get('corsi_for_pct', 50.0) / 100.0
        
        away_gf = away_stats.get('goals_per_game', 3.0)
        away_ga = away_stats.get('goals_against_per_game', 3.0)
        away_xgf_pct = away_stats.get('xGF_pct', 50.0) / 100.0
        away_corsi = away_stats.get('corsi_for_pct', 50.0) / 100.0
        
        # Calculate expected goals (average of offense vs defense)
        # Home expected: (Home GF + Away GA) / 2, adjusted for home ice
        home_ice_boost = 1.08  # 8% home ice advantage
        expected_home = ((home_gf + away_ga) / 2) * home_ice_boost
        expected_away = (away_gf + home_ga) / 2
        
        # Factor in advanced stats (xGF%, Corsi)
        home_quality = (home_xgf_pct + home_corsi) / 2
        away_quality = (away_xgf_pct + away_corsi) / 2
        
        # Adjust expectations by quality
        expected_home *= (0.8 + home_quality * 0.4)  # 0.8-1.2x multiplier
        expected_away *= (0.8 + away_quality * 0.4)
        
        # Calculate win probability using Poisson-based estimation
        # Simplified: team with more expected goals has proportional advantage
        goal_diff = expected_home - expected_away
        
        # Win prob formula (sigmoid-like)
        # Each goal of advantage = ~15% swing
        home_win_base = 0.54  # Base home ice advantage
        home_win_prob = home_win_base + (goal_diff * 0.15)
        
        # Factor in possession metrics
        possession_diff = (home_corsi - away_corsi)
        home_win_prob += possession_diff * 0.1
        
        # Clip to valid range but allow for lopsided games
        home_win_prob = float(np.clip(home_win_prob, 0.15, 0.85))
        
        # Calculate confidence based on stat differential
        stat_diff = abs(home_quality - away_quality)
        confidence = 0.65 + (stat_diff * 0.35)  # 0.65-1.0
        confidence = float(np.clip(confidence, 0.5, 0.95))
        
        return {
            'home_win_prob': home_win_prob,
            'away_win_prob': 1 - home_win_prob,
            'expected_goals_home': float(np.clip(expected_home, 1.5, 5.0)),
            'expected_goals_away': float(np.clip(expected_away, 1.5, 5.0)),
            'confidence': confidence,
            'model_version': self.version
        }
    
    def _simple_prediction(self, game_state: Dict[str, Any]) -> float:
        """
        Simplified prediction for MVP.
        
        TODO: Build proper features and use actual model.
        For now, use basic heuristics.
        """
        # Base home advantage
        home_prob = 0.55
        
        # Adjust for score
        score_diff = game_state.get('score_home', 0) - game_state.get('score_away', 0)
        home_prob += score_diff * 0.15
        
        # Adjust for time
        time_remaining = game_state.get('time_remaining', 60)
        time_factor = (60 - time_remaining) / 60
        home_prob += time_factor * 0.05
        
        # Clip to valid range
        return np.clip(home_prob, 0.0, 1.0)
    
    def recommend_decision(
        self,
        decision_type: str,
        options: list,
        game_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recommend best decision from available options.
        
        Args:
            decision_type: Type of decision ('line_change', 'pull_goalie', etc.)
            options: List of available options
            game_state: Current game state
        
        Returns:
            Dictionary with recommended option and reasoning
        """
        # For MVP, use simple heuristics
        # TODO: Use model to evaluate each option
        
        if decision_type == 'line_change':
            return self._recommend_line_change(game_state)
        elif decision_type == 'pull_goalie':
            return self._recommend_pull_goalie(game_state)
        else:
            return {
                'recommendation': options[0] if options else None,
                'confidence': 0.5,
                'reasoning': 'Default recommendation'
            }
    
    def _recommend_line_change(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend whether to change lines."""
        time_since_change = game_state.get('time_since_last_change', 0)
        fatigue = game_state.get('current_line_fatigue', 0)
        
        should_change = time_since_change > 1.5 or fatigue > 0.7
        
        return {
            'recommendation': 'change_lines' if should_change else 'keep_lines',
            'confidence': 0.8 if should_change else 0.6,
            'reasoning': f'Time since change: {time_since_change:.1f}min, Fatigue: {fatigue:.1f}'
        }
    
    def _recommend_pull_goalie(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend whether to pull goalie."""
        score_diff = game_state.get('score_home', 0) - game_state.get('score_away', 0)
        time_remaining = game_state.get('time_remaining', 60)
        
        # Trailing by 1-2, less than 2 minutes left
        should_pull = score_diff in [-1, -2] and time_remaining < 2.0
        
        return {
            'recommendation': 'pull_goalie' if should_pull else 'keep_goalie',
            'confidence': 0.9 if abs(score_diff) == 1 and time_remaining < 1.5 else 0.6,
            'reasoning': f'Score diff: {score_diff}, Time: {time_remaining:.1f}min'
        }
    
    def get_version(self) -> str:
        """Get current model version."""
        return self.version
    
    def get_info(self) -> Dict[str, Any]:
        """Get model information."""
        return {
            'version': self.version,
            'model_type': 'LogisticRegression',
            'features_count': len(self.dataset.features.columns) if self.dataset else 0,
            'training_games': len(self.dataset.games) if self.dataset else 0,
            'status': 'ready'
        }


# Singleton instance
_client_instance = None

def get_puckcast_client() -> PuckcastClient:
    """Get or create singleton Puckcast client."""
    global _client_instance
    if _client_instance is None:
        _client_instance = PuckcastClient()
    return _client_instance

