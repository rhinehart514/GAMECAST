"""
Test API Prediction Directly

Debug script to test the Intelligence Service API directly.
"""

import sys
import io
import httpx
import json

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from nhl_loader import load_all_teams
from nhl_data import NHL_TEAMS


def test_api_prediction():
    """Test calling the prediction API directly."""
    
    print("="*70)
    print("API PREDICTION TEST")
    print("="*70)
    print()
    
    # Load teams
    print("Loading NHL teams...")
    load_all_teams()
    tor = NHL_TEAMS['TOR']
    mtl = NHL_TEAMS['MTL']
    print(f"✅ Loaded {len(NHL_TEAMS)} teams\n")
    
    # Build request payload
    payload = {
        "home_team_id": tor.code,
        "away_team_id": mtl.code,
        "period": 1,
        "time_remaining": 60.0,
        "score_home": 0,
        "score_away": 0,
        "home_stats": {
            "goals_per_game": tor.stats.goals_per_game,
            "goals_against_per_game": tor.stats.goals_against_per_game,
            "xGF_pct": tor.stats.xGF_pct,
            "corsi_for_pct": tor.stats.corsi_for_pct,
        },
        "away_stats": {
            "goals_per_game": mtl.stats.goals_per_game,
            "goals_against_per_game": mtl.stats.goals_against_per_game,
            "xGF_pct": mtl.stats.xGF_pct,
            "corsi_for_pct": mtl.stats.corsi_for_pct,
        }
    }
    
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    print()
    
    # Test API call
    print("Calling http://localhost:8000/predict-game...")
    try:
        client = httpx.Client(timeout=10.0)
        response = client.post(
            "http://localhost:8000/predict-game",
            json=payload
        )
        
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print()
            print("Response:")
            print(json.dumps(result, indent=2))
            print()
            print(f"Home Win Probability: {result['home_win_prob']*100:.1f}%")
            print(f"Expected Score: {result['expected_goals_home']:.1f} - {result['expected_goals_away']:.1f}")
            print(f"Confidence: {result['confidence']*100:.0f}%")
        else:
            print("❌ ERROR!")
            print()
            print("Response:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_api_prediction()



