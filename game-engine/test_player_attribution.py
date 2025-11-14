"""
Test script for player-level event attribution.
Validates that goals are attributed to specific players.
"""

import sys
from pathlib import Path

# Add game-engine to path
sys.path.insert(0, str(Path(__file__).parent))

from simulator import NHLSimulator
from nhl_loader import load_all_teams

def test_player_attribution():
    """Test that player attribution works correctly."""
    
    print("=" * 80)
    print("TESTING PLAYER-LEVEL EVENT ATTRIBUTION")
    print("=" * 80)
    
    # Load NHL teams
    print("\n1. Loading NHL team data...")
    load_all_teams()
    print("   ✓ Teams loaded")
    
    # Create simulator
    print("\n2. Creating simulator...")
    sim = NHLSimulator(
        api_url="http://localhost:5001",
        verbose=True,
        home_ice_advantage=1.05
    )
    print("   ✓ Simulator ready")
    
    # Simulate a game between two strong teams
    print("\n3. Simulating game: Toronto Maple Leafs vs Boston Bruins")
    print("-" * 80)
    
    game = sim.simulate_game("TOR", "BOS")
    
    print("-" * 80)
    print("\n4. Validating Results...")
    
    # Check period scores exist
    assert len(game.period_scores) > 0, "No period scores found!"
    print(f"   ✓ Period scores tracked: {len(game.period_scores)} periods")
    
    # Check for goals with player attribution
    total_goals = 0
    goals_with_scorer = 0
    goals_with_assists = 0
    
    print("\n5. Goal Details:")
    print("-" * 80)
    
    for period_num, period_score in sorted(game.period_scores.items()):
        if period_score.goals:
            print(f"\n   Period {period_num}:")
            for goal in period_score.goals:
                total_goals += 1
                scorer = goal.get('scorer', 'Unknown')
                primary = goal.get('primary_assist')
                secondary = goal.get('secondary_assist')
                team = goal.get('team')
                time = goal.get('time_elapsed', 0)
                mins = time // 60
                secs = time % 60
                is_pp = goal.get('is_power_play', False)
                is_en = goal.get('is_empty_net', False)
                
                if scorer != 'Unknown':
                    goals_with_scorer += 1
                
                if primary or secondary:
                    goals_with_assists += 1
                
                # Print goal details
                goal_desc = f"   [{mins:02d}:{secs:02d}] {team} - {scorer}"
                if primary or secondary:
                    assists = [a for a in [primary, secondary] if a]
                    goal_desc += f" ({', '.join(assists)})"
                if is_pp:
                    goal_desc += " [PP]"
                if is_en:
                    goal_desc += " [EN]"
                print(goal_desc)
    
    print("\n" + "-" * 80)
    print("\n6. Validation Summary:")
    print(f"   Total Goals:           {total_goals}")
    print(f"   Goals with Scorer:     {goals_with_scorer} ({goals_with_scorer/total_goals*100 if total_goals > 0 else 0:.0f}%)")
    print(f"   Goals with Assists:    {goals_with_assists} ({goals_with_assists/total_goals*100 if total_goals > 0 else 0:.0f}%)")
    
    # Assertions
    assert total_goals > 0, "No goals scored in game!"
    assert goals_with_scorer > 0, "No goals attributed to players!"
    
    success_rate = goals_with_scorer / total_goals
    assert success_rate > 0.9, f"Too many goals without attribution: {success_rate:.0%}"
    
    print("\n   ✓ All validations passed!")
    
    # Check final game state
    print(f"\n7. Final Score:")
    print(f"   {game.away_team.name}: {game.away_team.score}")
    print(f"   {game.home_team.name}: {game.home_team.score}")
    print(f"   Winner: {game.get_winner().name}")
    
    print("\n" + "=" * 80)
    print("✅ PLAYER ATTRIBUTION TEST PASSED")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    try:
        test_player_attribution()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


