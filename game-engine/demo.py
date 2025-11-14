"""
NHL Simulation Demo

Run this to see the game simulator in action!
"""

import sys
from pathlib import Path

# Add game-engine to path
sys.path.insert(0, str(Path(__file__).parent))

from simulator import NHLSimulator


def main():
    """Run demo simulations."""
    print("\n" + "="*70)
    print("NHL GAME SIMULATOR - DEMO")
    print("AI-Powered Hockey Simulation")
    print("="*70)
    
    # Initialize simulator
    print("\nInitializing simulator...")
    print("Connecting to Intelligence Service at http://localhost:8000...")
    
    simulator = NHLSimulator(
        api_url="http://localhost:8000",
        verbose=True
    )
    
    print("\n[OK] Simulator ready!\n")
    
    # Demo games
    games = [
        {
            "home_code": "TOR",
            "home_name": "Toronto Maple Leafs",
            "away_code": "MTL",
            "away_name": "Montreal Canadiens"
        },
        {
            "home_code": "BOS",
            "home_name": "Boston Bruins",
            "away_code": "NYR",
            "away_name": "New York Rangers"
        },
        {
            "home_code": "EDM",
            "home_name": "Edmonton Oilers",
            "away_code": "CGY",
            "away_name": "Calgary Flames"
        }
    ]
    
    print("Select a game to simulate:\n")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game['away_name']} @ {game['home_name']}")
    print(f"{len(games) + 1}. Simulate all games")
    print(f"{len(games) + 2}. Custom game")
    
    try:
        choice = int(input("\nEnter choice: "))
        
        if choice == len(games) + 1:
            # Simulate all
            results = []
            for game in games:
                result = simulator.simulate_game(
                    home_team_code=game['home_code'],
                    home_team_name=game['home_name'],
                    away_team_code=game['away_code'],
                    away_team_name=game['away_name']
                )
                results.append(result)
                input("\nPress Enter to continue to next game...")
            
            # Print summary
            print("\n" + "="*70)
            print("SIMULATION SUMMARY")
            print("="*70)
            for result in results:
                winner = result.get_winner()
                print(f"{result.away_team.name} {result.away_team.score} - {result.home_team.score} {result.home_team.name} (Winner: {winner.name})")
            print("="*70)
            
        elif choice == len(games) + 2:
            # Custom game
            print("\nCustom Game Setup")
            home_code = input("Home team code (e.g., TOR): ").upper()
            home_name = input("Home team name: ")
            away_code = input("Away team code (e.g., MTL): ").upper()
            away_name = input("Away team name: ")
            
            simulator.simulate_game(
                home_team_code=home_code,
                home_team_name=home_name,
                away_team_code=away_code,
                away_team_name=away_name
            )
        
        elif 1 <= choice <= len(games):
            # Single game
            game = games[choice - 1]
            simulator.simulate_game(
                home_team_code=game['home_code'],
                home_team_name=game['home_name'],
                away_team_code=game['away_code'],
                away_team_name=game['away_name']
            )
        else:
            print("Invalid choice!")
            return
        
        print("\n[SUCCESS] Simulation complete!")
        
    except ValueError:
        print("Invalid input!")
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure the Intelligence Service is running:")
        print("  cd intelligence-service/src")
        print("  python main.py")


if __name__ == "__main__":
    main()

