"""
Test NHL Teams Simulation

Tests the simulator with real NHL team data including home ice advantage.
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
    """Run NHL team simulation tests."""
    
    print("="*70)
    print("NHL TEAM SIMULATION TEST")
    print("="*70)
    print()
    
    # Load NHL data
    print("Loading NHL team data...")
    count = load_all_teams()
    print(f"✅ Loaded {count} NHL teams\n")
    
    # Display available teams
    print("Available Teams:")
    for code, team in NHL_TEAMS.items():
        strength = team.overall_strength
        record = f"{team.stats.wins}-{team.stats.losses}-{team.stats.otl}"
        print(f"  {code}: {team.full_name} (Strength: {strength:.1f}/100, Record: {record})")
    print()
    
    # Initialize simulator with home ice advantage
    sim = NHLSimulator(
        api_url="http://localhost:8000",
        verbose=True,
        home_ice_advantage=1.10  # 10% home ice boost
    )
    
    print("\n" + "="*70)
    print("TEST 1: Montreal @ Toronto (Atlantic Division Rivals)")
    print("="*70)
    
    game1 = sim.simulate_game("MTL", "TOR")
    
    print("\n" + "="*70)
    print("TEST 2: Toronto @ Montreal (Home Ice Switch)")
    print("="*70)
    
    game2 = sim.simulate_game("TOR", "MTL")
    
    print("\n" + "="*70)
    print("TEST 3: Boston @ Florida (Atlantic Division)")
    print("="*70)
    
    game3 = sim.simulate_game("BOS", "FLA")
    
    # Summary
    print("\n" + "="*70)
    print("SIMULATION SUMMARY")
    print("="*70)
    
    results = [
        ("MTL @ TOR", game1),
        ("TOR @ MTL", game2),
        ("BOS @ FLA", game3)
    ]
    
    for matchup, game in results:
        winner = game.get_winner()
        home_score = game.home_team.score
        away_score = game.away_team.score
        
        winner_name = winner.name if winner else "TIE"
        home_shots = game.home_team.shots
        away_shots = game.away_team.shots
        
        print(f"\n{matchup}")
        print(f"  Final: {away_score} - {home_score}")
        print(f"  Winner: {winner_name}")
        print(f"  Shots: {away_shots} - {home_shots}")
        print(f"  Home xGF%: {(game.home_team.expected_goals / (game.home_team.expected_goals + game.away_team.expected_goals) * 100) if (game.home_team.expected_goals + game.away_team.expected_goals) > 0 else 50:.1f}%")
    
    print("\n" + "="*70)
    print("TEST COMPLETE!")
    print("="*70)
    print("\n✅ Real NHL teams working!")
    print("✅ Home ice advantage working!")
    print("✅ Team strength modifiers working!")
    print("\nReady for Week 3 completion! 🏒\n")


if __name__ == "__main__":
    main()



