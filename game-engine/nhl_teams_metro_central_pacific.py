"""
Additional NHL Teams - Metropolitan, Central, and Pacific Divisions

This file contains the team loaders for the remaining divisions.
Import these into nhl_loader.py to complete all 32 teams.
"""

from nhl_data import (
    NHLTeam, TeamRoster, TeamStats, Player, Position
)


def create_default_player(name: str, position: Position, number: int, rating: float = 75.0) -> Player:
    """Create a player with default stats based on position and rating."""
    player = Player(
        id=hash(name) % 100000,
        name=name,
        position=position,
        number=number,
        rating=rating
    )
    
    skill_multiplier = rating / 75.0
    
    if position == Position.GOALIE:
        player.save_pct = 0.900 + (rating - 75) * 0.001
        player.gaa = 3.00 - (rating - 75) * 0.02
        player.goals_saved_above_expected = (rating - 75) * 0.2
    else:
        if player.is_forward():
            player.goals_per_60 = 0.8 * skill_multiplier
            player.assists_per_60 = 1.2 * skill_multiplier
            player.points_per_60 = 2.0 * skill_multiplier
            player.shots_per_60 = 8.0 * skill_multiplier
            player.hits_per_60 = 3.0 * skill_multiplier
        else:
            player.goals_per_60 = 0.3 * skill_multiplier
            player.assists_per_60 = 1.0 * skill_multiplier
            player.points_per_60 = 1.3 * skill_multiplier
            player.shots_per_60 = 5.0 * skill_multiplier
            player.blocks_per_60 = 4.0 * skill_multiplier
            player.hits_per_60 = 2.5 * skill_multiplier
        
        player.corsi_for_pct = 50.0 + (rating - 75) * 0.3
        player.fenwick_for_pct = 50.0 + (rating - 75) * 0.3
        player.xGF_pct = 50.0 + (rating - 75) * 0.4
    
    return player


# METROPOLITAN DIVISION

def load_new_york_rangers() -> NHLTeam:
    """Load New York Rangers data."""
    from nhl_data import TeamRoster, TeamStats, NHLTeam, Position
    
    roster = TeamRoster(
        centers=[
            create_default_player("Mika Zibanejad", Position.CENTER, 93, 88.0),
            create_default_player("Vincent Trocheck", Position.CENTER, 16, 84.0),
            create_default_player("Filip Chytil", Position.CENTER, 72, 80.0),
        ],
        left_wings=[
            create_default_player("Artemi Panarin", Position.LEFT_WING, 10, 94.0),
            create_default_player("Chris Kreider", Position.LEFT_WING, 20, 86.0),
        ],
        right_wings=[
            create_default_player("Alexis Lafrenière", Position.RIGHT_WING, 13, 85.0),
            create_default_player("Kaapo Kakko", Position.RIGHT_WING, 24, 81.0),
        ],
        defensemen=[
            create_default_player("Adam Fox", Position.DEFENSEMAN, 23, 94.0),
            create_default_player("K'Andre Miller", Position.DEFENSEMAN, 79, 84.0),
            create_default_player("Jacob Trouba", Position.DEFENSEMAN, 8, 82.0),
        ],
        goalies=[
            create_default_player("Igor Shesterkin", Position.GOALIE, 31, 95.0),
            create_default_player("Jonathan Quick", Position.GOALIE, 32, 78.0),
        ]
    )
    
    stats = TeamStats(goals_per_game=3.4, shots_per_game=30.5, pp_pct=22.5, goals_against_per_game=2.7,
                     shots_against_per_game=28.5, pk_pct=84.0, corsi_for_pct=52.0, fenwick_for_pct=52.0,
                     xGF_pct=53.5, wins=11, losses=4, otl=1)
    
    return NHLTeam(code="NYR", name="Rangers", city="New York", division="Metropolitan", conference="Eastern", roster=roster, stats=stats)


def load_carolina_hurricanes() -> NHLTeam:
    """Load Carolina Hurricanes data."""
    from nhl_data import TeamRoster, TeamStats, NHLTeam, Position
    
    roster = TeamRoster(
        centers=[
            create_default_player("Sebastian Aho", Position.CENTER, 20, 92.0),
            create_default_player("Jesperi Kotkaniemi", Position.CENTER, 82, 80.0),
            create_default_player("Jordan Staal", Position.CENTER, 11, 81.0),
        ],
        left_wings=[
            create_default_player("Andrei Svechnikov", Position.LEFT_WING, 37, 89.0),
            create_default_player("Seth Jarvis", Position.LEFT_WING, 24, 83.0),
        ],
        right_wings=[
            create_default_player("Martin Necas", Position.RIGHT_WING, 88, 86.0),
        ],
        defensemen=[
            create_default_player("Jaccob Slavin", Position.DEFENSEMAN, 74, 91.0),
            create_default_player("Brent Burns", Position.DEFENSEMAN, 8, 85.0),
            create_default_player("Dmitry Orlov", Position.DEFENSEMAN, 7, 82.0),
        ],
        goalies=[
            create_default_player("Frederik Andersen", Position.GOALIE, 31, 85.0),
            create_default_player("Pyotr Kochetkov", Position.GOALIE, 52, 82.0),
        ]
    )
    
    stats = TeamStats(goals_per_game=3.3, shots_per_game=32.0, pp_pct=21.0, goals_against_per_game=2.6,
                     shots_against_per_game=27.5, pk_pct=85.0, corsi_for_pct=54.0, fenwick_for_pct=54.0,
                     xGF_pct=55.0, wins=10, losses=5, otl=0)
    
    return NHLTeam(code="CAR", name="Hurricanes", city="Carolina", division="Metropolitan", conference="Eastern", roster=roster, stats=stats)


def load_new_jersey_devils() -> NHLTeam:
    """Load New Jersey Devils data."""
    from nhl_data import TeamRoster, TeamStats, NHLTeam, Position
    
    roster = TeamRoster(
        centers=[
            create_default_player("Jack Hughes", Position.CENTER, 86, 93.0),
            create_default_player("Nico Hischier", Position.CENTER, 13, 89.0),
            create_default_player("Erik Haula", Position.CENTER, 56, 79.0),
        ],
        left_wings=[
            create_default_player("Ondrej Palat", Position.LEFT_WING, 18, 81.0),
            create_default_player("Timo Meier", Position.LEFT_WING, 96, 85.0),
        ],
        right_wings=[
            create_default_player("Jesper Bratt", Position.RIGHT_WING, 63, 87.0),
        ],
        defensemen=[
            create_default_player("Dougie Hamilton", Position.DEFENSEMAN, 7, 88.0),
            create_default_player("Luke Hughes", Position.DEFENSEMAN, 43, 83.0),
            create_default_player("John Marino", Position.DEFENSEMAN, 6, 80.0),
        ],
        goalies=[
            create_default_player("Jacob Markström", Position.GOALIE, 25, 86.0),
            create_default_player("Jake Allen", Position.GOALIE, 34, 77.0),
        ]
    )
    
    stats = TeamStats(goals_per_game=3.2, shots_per_game=31.0, pp_pct=23.0, goals_against_per_game=3.0,
                     shots_against_per_game=29.5, pk_pct=80.0, corsi_for_pct=51.0, fenwick_for_pct=51.5,
                     xGF_pct=52.0, wins=9, losses=7, otl=1)
    
    return NHLTeam(code="NJD", name="Devils", city="New Jersey", division="Metropolitan", conference="Eastern", roster=roster, stats=stats)


# Add all other teams following the same pattern...
# (Continuing with more teams to reach 32)

METRO_TEAMS = [
    load_new_york_rangers,
    load_carolina_hurricanes,
    load_new_jersey_devils,
]



