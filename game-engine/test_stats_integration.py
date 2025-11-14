#!/usr/bin/env python3
"""
Test script to verify player stats tracking integration with season simulator.
"""
import sys
import io

# Set up UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from season_simulator import SeasonSimulator

def test_player_stats_tracking():
    """Test that player stats are properly tracked during season simulation."""
    print("\n" + "="*70)
    print("TESTING PLAYER STATS TRACKING INTEGRATION")
    print("="*70 + "\n")
    
    # Create season simulator
    print("📊 Creating season simulator...")
    simulator = SeasonSimulator(season_year="2024-25", verbose=False)
    
    # Simulate a small number of games
    num_games = 50
    print(f"🏒 Simulating {num_games} games...\n")
    simulator.simulate_season(num_games=num_games)
    
    # Check if stats tracker has data
    print("\n" + "="*70)
    print("PLAYER STATISTICS SUMMARY")
    print("="*70 + "\n")
    
    # Get top scorers
    print("🏆 TOP 10 POINTS LEADERS")
    print("-" * 70)
    leaders = simulator.stats_tracker.get_league_leaders(stat='points', limit=10, min_games=1)
    
    if not leaders:
        print("❌ ERROR: No player stats found!")
        return False
    
    print(f"{'#':<4} {'Player':<25} {'Team':<6} {'GP':<5} {'G':<5} {'A':<5} {'PTS':<6}")
    print("-" * 70)
    for i, player in enumerate(leaders):
        print(f"{i+1:<4} {player.player_name:<25} {player.team_code:<6} "
              f"{player.games_played:<5} {player.goals:<5} {player.assists:<5} {player.points:<6}")
    
    print("\n" + "="*70)
    print("🎯 TOP 5 GOAL SCORERS")
    print("-" * 70)
    goal_leaders = simulator.stats_tracker.get_league_leaders(stat='goals', limit=5, min_games=1)
    
    for i, player in enumerate(goal_leaders):
        print(f"{i+1}. {player.player_name} ({player.team_code}) - {player.goals} goals")
    
    print("\n" + "="*70)
    print("🎯 TOP 5 ASSIST LEADERS")
    print("-" * 70)
    assist_leaders = simulator.stats_tracker.get_league_leaders(stat='assists', limit=5, min_games=1)
    
    for i, player in enumerate(assist_leaders):
        print(f"{i+1}. {player.player_name} ({player.team_code}) - {player.assists} assists")
    
    # Show a team's roster stats
    print("\n" + "="*70)
    print("📊 SAMPLE TEAM ROSTER STATS (TOR)")
    print("-" * 70)
    tor_stats = simulator.stats_tracker.get_team_stats('TOR')
    
    print(f"{'Player':<25} {'GP':<5} {'G':<5} {'A':<5} {'PTS':<6}")
    print("-" * 70)
    for player in tor_stats[:10]:  # Top 10 for Toronto
        print(f"{player.player_name:<25} {player.games_played:<5} "
              f"{player.goals:<5} {player.assists:<5} {player.points:<6}")
    
    print("\n" + "="*70)
    print("✅ PLAYER STATS TRACKING INTEGRATION: SUCCESS!")
    print("="*70 + "\n")
    
    print("📈 Summary:")
    print(f"   • Total unique players tracked: {len(simulator.stats_tracker.player_stats)}")
    print(f"   • Games simulated: {num_games}")
    print(f"   • Top scorer: {leaders[0].player_name} ({leaders[0].points} pts)")
    print(f"   • Integration status: ✅ WORKING")
    
    return True

if __name__ == "__main__":
    success = test_player_stats_tracking()
    sys.exit(0 if success else 1)

