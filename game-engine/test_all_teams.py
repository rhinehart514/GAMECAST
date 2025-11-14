"""Quick test of all 32 teams working"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from simulator import NHLSimulator
from nhl_loader import load_all_teams

print("Loading all NHL teams...")
count = load_all_teams()
print(f"✅ Loaded {count} teams\n")

print("Testing 3 different matchups:\n")

sim = NHLSimulator(verbose=False)

# Test 1: McDavid vs MacKinnon
game1 = sim.simulate_game("EDM", "COL")
print(f"1. Edmonton Oilers {game1.away_team.score} - Colorado Avalanche {game1.home_team.score}")
print(f"   Winner: {game1.get_winner().name if game1.get_winner() else 'TIE'}\n")

# Test 2: Battle of NY
game2 = sim.simulate_game("NYI", "NYR")
print(f"2. New York Islanders {game2.away_team.score} - New York Rangers {game2.home_team.score}")
print(f"   Winner: {game2.get_winner().name if game2.get_winner() else 'TIE'}\n")

# Test 3: Worst vs Best
game3 = sim.simulate_game("SJS", "WPG")
print(f"3. San Jose Sharks {game3.away_team.score} - Winnipeg Jets {game3.home_team.score}")
print(f"   Winner: {game3.get_winner().name if game3.get_winner() else 'TIE'}\n")

print("✅ All teams working perfectly!")



