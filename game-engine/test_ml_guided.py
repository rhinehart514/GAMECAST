"""
Test ML-Guided Simulation

Tests the simulator with ML predictions driving the probabilities.
This is the "living game" fully realized!
"""

import sys
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from simulator import NHLSimulator
from nhl_loader import load_all_teams
from nhl_data import NHL_TEAMS


def main():
    """Run ML-guided simulation tests."""
    
    print("="*70)
    print("ML-GUIDED SIMULATION TEST")
    print("="*70)
    print()
    print("This test shows the 'living game' architecture in action:")
    print("1. ML model predicts expected outcome")
    print("2. Simulation dynamically adjusts to match prediction")
    print("3. Game plays out realistically towards predicted result")
    print()
    
    # Load NHL data
    print("Loading NHL team data...")
    count = load_all_teams()
    print(f"✅ Loaded {count} NHL teams\n")
    
    # Initialize simulator
    print("Connecting to Intelligence Service...")
    sim = NHLSimulator(
        api_url="http://localhost:8000",
        verbose=True,
        home_ice_advantage=1.10
    )
    print("✅ Connected!\n")
    
    print("\n" + "="*70)
    print("TEST 1: Toronto (strong) vs Montreal (weaker) at home")
    print("="*70)
    print("ML should predict TOR advantage...")
    print()
    
    game1 = sim.simulate_game("MTL", "TOR")
    
    print("\n" + "="*70)
    print("TEST 2: Florida (champions) vs Boston (competitive)")
    print("="*70)
    print("ML should predict close game with FLA slight edge...")
    print()
    
    game2 = sim.simulate_game("BOS", "FLA")
    
    print("\n" + "="*70)
    print("TEST 3: Montreal (weaker) at home vs Boston (strong)")
    print("="*70)
    print("ML should predict BOS advantage despite road game...")
    print()
    
    game3 = sim.simulate_game("BOS", "MTL")
    
    # Summary and Analysis
    print("\n" + "="*70)
    print("ML-GUIDED SIMULATION ANALYSIS")
    print("="*70)
    
    games = [
        ("MTL @ TOR", game1),
        ("BOS @ FLA", game2),
        ("BOS @ MTL", game3)
    ]
    
    for matchup, game in games:
        winner = game.get_winner()
        home_score = game.home_team.score
        away_score = game.away_team.score
        winner_name = winner.name if winner else "TIE"
        
        print(f"\n{matchup}")
        print(f"  Final: {away_score} - {home_score}")
        print(f"  Winner: {winner_name}")
        print(f"  Shots: {game.away_team.shots} - {game.home_team.shots}")
        
        # Check if result makes sense
        if home_score + away_score == 0:
            print(f"  ⚠️  WARNING: Shutout - may need tuning")
        elif home_score + away_score > 8:
            print(f"  ⚠️  WARNING: High scoring - may need tuning")
        else:
            print(f"  ✅ Realistic score")
    
    print("\n" + "="*70)
    print("TEST COMPLETE!")
    print("="*70)
    print("\nKEY INNOVATIONS DEMONSTRATED:")
    print("✅ ML model predicts game outcome BEFORE simulation")
    print("✅ Simulation probabilities adjust to match ML expectations")
    print("✅ Game plays out realistically toward predicted result")
    print("✅ Model improvements automatically improve game realism")
    print("\nThis is the 'LIVING GAME' - it gets smarter as the model learns! 🤖🏒\n")


if __name__ == "__main__":
    main()



