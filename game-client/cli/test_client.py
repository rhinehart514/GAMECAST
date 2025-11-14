"""
Simple CLI client to test the intelligence service.

Usage:
    python test_client.py
"""

import httpx
import json
from datetime import datetime


API_URL = "http://localhost:8000"


def print_header(text):
    """Print a nice header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def test_health():
    """Test health endpoint."""
    print_header("Testing Health Endpoint")
    
    try:
        response = httpx.get(f"{API_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print("[OK] Service is healthy")
        print(f"   Model version: {data['model_version']}")
        print(f"   Status: {data['status']}")
        print(f"   Timestamp: {data['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return False


def test_prediction():
    """Test game prediction endpoint."""
    print_header("Testing Game Prediction")
    
    # Scenario: Close game in 3rd period
    game_state = {
        "home_team_id": 6,  # Boston
        "away_team_id": 10, # Toronto
        "period": 3,
        "time_remaining": 5.0,
        "score_home": 2,
        "score_away": 2,
        "home_fatigue": 0.6,
        "away_fatigue": 0.4
    }
    
    print("Scenario: Close game in 3rd period")
    print(f"  Boston (home) vs Toronto (away)")
    print(f"  Score: {game_state['score_home']} - {game_state['score_away']}")
    print(f"  Time: {game_state['time_remaining']:.1f} min remaining in period {game_state['period']}")
    print()
    
    try:
        response = httpx.post(
            f"{API_URL}/predict-game",
            json=game_state,
            timeout=10.0
        )
        response.raise_for_status()
        
        data = response.json()
        
        print("[OK] Prediction received:")
        print(f"   Home win probability: {data['home_win_prob']:.1%}")
        print(f"   Away win probability: {data['away_win_prob']:.1%}")
        print(f"   Expected goals (home): {data['expected_goals_home']:.2f}")
        print(f"   Expected goals (away): {data['expected_goals_away']:.2f}")
        print(f"   Confidence: {data['confidence']:.1%}")
        print(f"   Model version: {data['model_version']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return False


def test_decision():
    """Test decision recommendation endpoint."""
    print_header("Testing Decision Recommendation")
    
    game_state = {
        "home_team_id": 6,
        "away_team_id": 10,
        "period": 3,
        "time_remaining": 1.5,
        "score_home": 2,
        "score_away": 3,  # Home team trailing
        "time_since_last_change": 2.0,
        "current_line_fatigue": 0.8
    }
    
    print("Scenario: Should we pull the goalie?")
    print(f"  Score: Home 2 - Away 3 (trailing by 1)")
    print(f"  Time: {game_state['time_remaining']:.1f} min remaining")
    print()
    
    request = {
        "decision_type": "pull_goalie",
        "options": ["pull_goalie", "keep_goalie"],
        "game_state": game_state
    }
    
    try:
        response = httpx.post(
            f"{API_URL}/recommend-decision",
            json=request,
            timeout=10.0
        )
        response.raise_for_status()
        
        data = response.json()
        
        print("[OK] Decision recommendation:")
        print(f"   Recommendation: {data['recommendation']}")
        print(f"   Confidence: {data['confidence']:.1%}")
        print(f"   Reasoning: {data['reasoning']}")
        print(f"   Model version: {data['model_version']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Decision request failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n[NHL Intelligence Service - Test Client]")
    print(f"   Testing API at: {API_URL}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    health_ok = test_health()
    
    if not health_ok:
        print("\n[ERROR] Service is not running or not healthy")
        print("\nTo start the service:")
        print("  cd intelligence-service")
        print("  python src/main.py")
        return
    
    test_prediction()
    test_decision()
    
    print("\n" + "=" * 70)
    print("[SUCCESS] All tests complete!")
    print("=" * 70)
    print("\nAPI documentation: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    main()

