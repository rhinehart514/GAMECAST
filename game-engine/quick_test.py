"""Quick test of the simulator."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from simulator import NHLSimulator

print("\n" + "="*70)
print("QUICK SIMULATION TEST")
print("="*70)

sim = NHLSimulator(api_url="http://localhost:8000", verbose=True)

game = sim.simulate_game(
    home_team_code="TOR",
    home_team_name="Toronto Maple Leafs",
    away_team_code="MTL",
    away_team_name="Montreal Canadiens"
)

print("\n[TEST] Simulation completed successfully!")
print(f"[TEST] Final score: {game.away_team.code} {game.away_team.score} - {game.home_team.score} {game.home_team.code}")
print(f"[TEST] Winner: {game.get_winner().name}")
print(f"[TEST] Total events: {len(game.events)}")

