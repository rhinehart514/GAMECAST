"""
NHL Data Loader

Loads real NHL team data for 2024-25 season.
Data based on current team performance and rosters.
"""

from nhl_data import (
    NHLTeam, TeamRoster, TeamStats, Player, Position, NHL_TEAMS
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
    
    # Scale stats based on rating (75 = average)
    skill_multiplier = rating / 75.0
    
    if position == Position.GOALIE:
        # Goalie stats
        player.save_pct = 0.900 + (rating - 75) * 0.001
        player.gaa = 3.00 - (rating - 75) * 0.02
        player.goals_saved_above_expected = (rating - 75) * 0.2
    else:
        # Skater stats (per 60 at 5v5)
        if player.is_forward():
            player.goals_per_60 = 0.8 * skill_multiplier
            player.assists_per_60 = 1.2 * skill_multiplier
            player.points_per_60 = 2.0 * skill_multiplier
            player.shots_per_60 = 8.0 * skill_multiplier
            player.hits_per_60 = 3.0 * skill_multiplier
        else:  # Defenseman
            player.goals_per_60 = 0.3 * skill_multiplier
            player.assists_per_60 = 1.0 * skill_multiplier
            player.points_per_60 = 1.3 * skill_multiplier
            player.shots_per_60 = 5.0 * skill_multiplier
            player.blocks_per_60 = 4.0 * skill_multiplier
            player.hits_per_60 = 2.5 * skill_multiplier
        
        # Two-way stats
        player.corsi_for_pct = 50.0 + (rating - 75) * 0.3
        player.fenwick_for_pct = 50.0 + (rating - 75) * 0.3
        player.xGF_pct = 50.0 + (rating - 75) * 0.4
    
    return player


def load_toronto_maple_leafs() -> NHLTeam:
    """Load Toronto Maple Leafs data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Auston Matthews", Position.CENTER, 34, 95.0),
            create_default_player("John Tavares", Position.CENTER, 91, 84.0),
            create_default_player("Max Domi", Position.CENTER, 11, 78.0),
            create_default_player("David Kampf", Position.CENTER, 64, 72.0),
        ],
        left_wings=[
            create_default_player("Matthew Knies", Position.LEFT_WING, 23, 80.0),
            create_default_player("Bobby McMann", Position.LEFT_WING, 74, 75.0),
        ],
        right_wings=[
            create_default_player("Mitch Marner", Position.RIGHT_WING, 16, 93.0),
            create_default_player("William Nylander", Position.RIGHT_WING, 88, 91.0),
        ],
        defensemen=[
            create_default_player("Morgan Rielly", Position.DEFENSEMAN, 44, 85.0),
            create_default_player("Chris Tanev", Position.DEFENSEMAN, 8, 83.0),
            create_default_player("Jake McCabe", Position.DEFENSEMAN, 22, 80.0),
            create_default_player("Oliver Ekman-Larsson", Position.DEFENSEMAN, 21, 77.0),
            create_default_player("Simon Benoit", Position.DEFENSEMAN, 2, 72.0),
            create_default_player("Conor Timmins", Position.DEFENSEMAN, 25, 71.0),
        ],
        goalies=[
            create_default_player("Joseph Woll", Position.GOALIE, 60, 82.0),
            create_default_player("Anthony Stolarz", Position.GOALIE, 41, 79.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=3.4,
        shots_per_game=32.5,
        pp_pct=24.5,
        goals_against_per_game=2.8,
        shots_against_per_game=29.0,
        pk_pct=82.0,
        corsi_for_pct=52.5,
        fenwick_for_pct=52.0,
        xGF_pct=53.0,
        wins=10,
        losses=6,
        otl=2
    )
    
    return NHLTeam(
        code="TOR",
        name="Maple Leafs",
        city="Toronto",
        division="Atlantic",
        conference="Eastern",
        roster=roster,
        stats=stats
    )


def load_montreal_canadiens() -> NHLTeam:
    """Load Montreal Canadiens data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Nick Suzuki", Position.CENTER, 14, 86.0),
            create_default_player("Kirby Dach", Position.CENTER, 77, 78.0),
            create_default_player("Christian Dvorak", Position.CENTER, 28, 74.0),
            create_default_player("Jake Evans", Position.CENTER, 71, 73.0),
        ],
        left_wings=[
            create_default_player("Cole Caufield", Position.LEFT_WING, 22, 88.0),
            create_default_player("Juraj Slafkovsky", Position.LEFT_WING, 20, 82.0),
        ],
        right_wings=[
            create_default_player("Brendan Gallagher", Position.RIGHT_WING, 11, 79.0),
            create_default_player("Joel Armia", Position.RIGHT_WING, 40, 74.0),
        ],
        defensemen=[
            create_default_player("Mike Matheson", Position.DEFENSEMAN, 8, 83.0),
            create_default_player("Kaiden Guhle", Position.DEFENSEMAN, 21, 81.0),
            create_default_player("Lane Hutson", Position.DEFENSEMAN, 48, 79.0),
            create_default_player("David Savard", Position.DEFENSEMAN, 58, 76.0),
            create_default_player("Jayden Struble", Position.DEFENSEMAN, 38, 72.0),
            create_default_player("Justin Barron", Position.DEFENSEMAN, 52, 71.0),
        ],
        goalies=[
            create_default_player("Sam Montembeault", Position.GOALIE, 35, 80.0),
            create_default_player("Cayden Primeau", Position.GOALIE, 30, 74.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=2.9,
        shots_per_game=30.5,
        pp_pct=19.5,
        goals_against_per_game=3.3,
        shots_against_per_game=31.0,
        pk_pct=78.0,
        corsi_for_pct=48.5,
        fenwick_for_pct=48.0,
        xGF_pct=47.5,
        wins=7,
        losses=10,
        otl=1
    )
    
    return NHLTeam(
        code="MTL",
        name="Canadiens",
        city="Montreal",
        division="Atlantic",
        conference="Eastern",
        roster=roster,
        stats=stats
    )


def load_boston_bruins() -> NHLTeam:
    """Load Boston Bruins data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Pavel Zacha", Position.CENTER, 18, 81.0),
            create_default_player("Charlie Coyle", Position.CENTER, 13, 79.0),
            create_default_player("Trent Frederic", Position.CENTER, 11, 76.0),
        ],
        left_wings=[
            create_default_player("Brad Marchand", Position.LEFT_WING, 63, 89.0),
            create_default_player("Morgan Geekie", Position.LEFT_WING, 39, 77.0),
        ],
        right_wings=[
            create_default_player("David Pastrnak", Position.RIGHT_WING, 88, 92.0),
            create_default_player("Justin Brazeau", Position.RIGHT_WING, 61, 76.0),
        ],
        defensemen=[
            create_default_player("Charlie McAvoy", Position.DEFENSEMAN, 73, 90.0),
            create_default_player("Hampus Lindholm", Position.DEFENSEMAN, 27, 85.0),
            create_default_player("Brandon Carlo", Position.DEFENSEMAN, 25, 80.0),
            create_default_player("Mason Lohrei", Position.DEFENSEMAN, 6, 77.0),
        ],
        goalies=[
            create_default_player("Jeremy Swayman", Position.GOALIE, 1, 87.0),
            create_default_player("Joonas Korpisalo", Position.GOALIE, 70, 76.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=3.2,
        shots_per_game=31.0,
        pp_pct=22.0,
        goals_against_per_game=2.9,
        shots_against_per_game=29.5,
        pk_pct=81.0,
        corsi_for_pct=51.0,
        fenwick_for_pct=51.5,
        xGF_pct=51.5,
        wins=9,
        losses=8,
        otl=1
    )
    
    return NHLTeam(
        code="BOS",
        name="Bruins",
        city="Boston",
        division="Atlantic",
        conference="Eastern",
        roster=roster,
        stats=stats
    )


def load_florida_panthers() -> NHLTeam:
    """Load Florida Panthers data (defending champions)."""
    roster = TeamRoster(
        centers=[
            create_default_player("Aleksander Barkov", Position.CENTER, 16, 93.0),
            create_default_player("Sam Bennett", Position.CENTER, 9, 84.0),
            create_default_player("Anton Lundell", Position.CENTER, 15, 80.0),
        ],
        left_wings=[
            create_default_player("Matthew Tkachuk", Position.LEFT_WING, 19, 92.0),
            create_default_player("Evan Rodrigues", Position.LEFT_WING, 17, 78.0),
        ],
        right_wings=[
            create_default_player("Sam Reinhart", Position.RIGHT_WING, 13, 91.0),
            create_default_player("Eetu Luostarinen", Position.RIGHT_WING, 27, 77.0),
        ],
        defensemen=[
            create_default_player("Gustav Forsling", Position.DEFENSEMAN, 42, 88.0),
            create_default_player("Aaron Ekblad", Position.DEFENSEMAN, 5, 85.0),
            create_default_player("Dmitry Kulikov", Position.DEFENSEMAN, 7, 79.0),
            create_default_player("Niko Mikkola", Position.DEFENSEMAN, 77, 78.0),
        ],
        goalies=[
            create_default_player("Sergei Bobrovsky", Position.GOALIE, 72, 88.0),
            create_default_player("Spencer Knight", Position.GOALIE, 30, 78.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=3.5,
        shots_per_game=32.0,
        pp_pct=23.0,
        goals_against_per_game=2.7,
        shots_against_per_game=28.5,
        pk_pct=83.5,
        corsi_for_pct=53.0,
        fenwick_for_pct=52.5,
        xGF_pct=54.0,
        wins=11,
        losses=5,
        otl=1
    )
    
    return NHLTeam(
        code="FLA",
        name="Panthers",
        city="Florida",
        division="Atlantic",
        conference="Eastern",
        roster=roster,
        stats=stats
    )


def load_tampa_bay_lightning() -> NHLTeam:
    """Load Tampa Bay Lightning data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Brayden Point", Position.CENTER, 21, 91.0),
            create_default_player("Anthony Cirelli", Position.CENTER, 71, 82.0),
            create_default_player("Nick Paul", Position.CENTER, 20, 78.0),
        ],
        left_wings=[
            create_default_player("Brandon Hagel", Position.LEFT_WING, 38, 85.0),
            create_default_player("Jake Guentzel", Position.LEFT_WING, 59, 88.0),
        ],
        right_wings=[
            create_default_player("Nikita Kucherov", Position.RIGHT_WING, 86, 95.0),
            create_default_player("Mitchell Chaffee", Position.RIGHT_WING, 68, 75.0),
        ],
        defensemen=[
            create_default_player("Victor Hedman", Position.DEFENSEMAN, 77, 92.0),
            create_default_player("Darren Raddysh", Position.DEFENSEMAN, 20, 79.0),
            create_default_player("Nick Perbix", Position.DEFENSEMAN, 44, 77.0),
            create_default_player("Erik Cernak", Position.DEFENSEMAN, 81, 80.0),
        ],
        goalies=[
            create_default_player("Andrei Vasilevskiy", Position.GOALIE, 88, 93.0),
            create_default_player("Jonas Johansson", Position.GOALIE, 32, 75.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=3.3,
        shots_per_game=30.0,
        pp_pct=23.5,
        goals_against_per_game=2.9,
        shots_against_per_game=29.0,
        pk_pct=82.5,
        corsi_for_pct=51.5,
        fenwick_for_pct=51.0,
        xGF_pct=52.0,
        wins=9,
        losses=6,
        otl=1
    )
    
    return NHLTeam(code="TBL", name="Lightning", city="Tampa Bay", division="Atlantic", conference="Eastern", roster=roster, stats=stats)


def load_ottawa_senators() -> NHLTeam:
    """Load Ottawa Senators data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Tim Stützle", Position.CENTER, 18, 89.0),
            create_default_player("Josh Norris", Position.CENTER, 9, 82.0),
            create_default_player("Shane Pinto", Position.CENTER, 12, 78.0),
        ],
        left_wings=[
            create_default_player("Brady Tkachuk", Position.LEFT_WING, 7, 88.0),
            create_default_player("Claude Giroux", Position.LEFT_WING, 28, 84.0),
        ],
        right_wings=[
            create_default_player("Drake Batherson", Position.RIGHT_WING, 19, 84.0),
        ],
        defensemen=[
            create_default_player("Thomas Chabot", Position.DEFENSEMAN, 72, 84.0),
            create_default_player("Jake Sanderson", Position.DEFENSEMAN, 85, 82.0),
            create_default_player("Nick Jensen", Position.DEFENSEMAN, 3, 78.0),
        ],
        goalies=[
            create_default_player("Linus Ullmark", Position.GOALIE, 35, 86.0),
            create_default_player("Anton Forsberg", Position.GOALIE, 31, 76.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=3.0,
        shots_per_game=29.0,
        pp_pct=20.0,
        goals_against_per_game=3.2,
        shots_against_per_game=31.0,
        pk_pct=77.5,
        corsi_for_pct=48.0,
        fenwick_for_pct=48.5,
        xGF_pct=48.5,
        wins=7,
        losses=8,
        otl=1
    )
    
    return NHLTeam(code="OTT", name="Senators", city="Ottawa", division="Atlantic", conference="Eastern", roster=roster, stats=stats)


def load_detroit_red_wings() -> NHLTeam:
    """Load Detroit Red Wings data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Dylan Larkin", Position.CENTER, 71, 87.0),
            create_default_player("J.T. Compher", Position.CENTER, 37, 79.0),
            create_default_player("Andrew Copp", Position.CENTER, 18, 78.0),
        ],
        left_wings=[
            create_default_player("Alex DeBrincat", Position.LEFT_WING, 93, 86.0),
            create_default_player("Lucas Raymond", Position.LEFT_WING, 23, 84.0),
        ],
        right_wings=[
            create_default_player("Patrick Kane", Position.RIGHT_WING, 88, 85.0),
            create_default_player("Vladimir Tarasenko", Position.RIGHT_WING, 91, 82.0),
        ],
        defensemen=[
            create_default_player("Moritz Seider", Position.DEFENSEMAN, 53, 88.0),
            create_default_player("Ben Chiarot", Position.DEFENSEMAN, 8, 79.0),
            create_default_player("Jeff Petry", Position.DEFENSEMAN, 46, 77.0),
        ],
        goalies=[
            create_default_player("Cam Talbot", Position.GOALIE, 39, 81.0),
            create_default_player("Ville Husso", Position.GOALIE, 35, 76.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=3.0,
        shots_per_game=28.5,
        pp_pct=21.0,
        goals_against_per_game=3.4,
        shots_against_per_game=31.5,
        pk_pct=76.0,
        corsi_for_pct=47.5,
        fenwick_for_pct=47.0,
        xGF_pct=47.0,
        wins=6,
        losses=8,
        otl=2
    )
    
    return NHLTeam(code="DET", name="Red Wings", city="Detroit", division="Atlantic", conference="Eastern", roster=roster, stats=stats)


def load_buffalo_sabres() -> NHLTeam:
    """Load Buffalo Sabres data."""
    roster = TeamRoster(
        centers=[
            create_default_player("Tage Thompson", Position.CENTER, 72, 88.0),
            create_default_player("Dylan Cozens", Position.CENTER, 24, 80.0),
            create_default_player("Peyton Krebs", Position.CENTER, 19, 75.0),
        ],
        left_wings=[
            create_default_player("Jeff Skinner", Position.LEFT_WING, 53, 82.0),
            create_default_player("Zach Benson", Position.LEFT_WING, 9, 76.0),
        ],
        right_wings=[
            create_default_player("Alex Tuch", Position.RIGHT_WING, 89, 83.0),
            create_default_player("JJ Peterka", Position.RIGHT_WING, 77, 80.0),
        ],
        defensemen=[
            create_default_player("Rasmus Dahlin", Position.DEFENSEMAN, 26, 90.0),
            create_default_player("Owen Power", Position.DEFENSEMAN, 25, 84.0),
            create_default_player("Bowen Byram", Position.DEFENSEMAN, 4, 81.0),
        ],
        goalies=[
            create_default_player("Ukko-Pekka Luukkonen", Position.GOALIE, 1, 83.0),
            create_default_player("Devon Levi", Position.GOALIE, 27, 77.0),
        ]
    )
    
    stats = TeamStats(
        goals_per_game=2.8,
        shots_per_game=29.5,
        pp_pct=18.0,
        goals_against_per_game=3.5,
        shots_against_per_game=32.0,
        pk_pct=75.0,
        corsi_for_pct=47.0,
        fenwick_for_pct=46.5,
        xGF_pct=46.0,
        wins=6,
        losses=9,
        otl=1
    )
    
    return NHLTeam(code="BUF", name="Sabres", city="Buffalo", division="Atlantic", conference="Eastern", roster=roster, stats=stats)


def load_team_from_data(code: str, data: dict) -> NHLTeam:
    """Load a team from compact data format."""
    roster = TeamRoster()
    
    # Parse players and add to roster
    for player_data in data["players"]:
        name, pos_str, number, rating = player_data
        
        # Convert position string to Position enum
        pos_map = {"C": Position.CENTER, "LW": Position.LEFT_WING, "RW": Position.RIGHT_WING,
                   "D": Position.DEFENSEMAN, "G": Position.GOALIE}
        position = pos_map[pos_str]
        
        player = create_default_player(name, position, number, rating)
        
        # Add to appropriate list
        if position == Position.CENTER:
            roster.centers.append(player)
        elif position == Position.LEFT_WING:
            roster.left_wings.append(player)
        elif position == Position.RIGHT_WING:
            roster.right_wings.append(player)
        elif position == Position.DEFENSEMAN:
            roster.defensemen.append(player)
        elif position == Position.GOALIE:
            roster.goalies.append(player)
    
    # Create stats from data
    s = data["stats"]
    stats = TeamStats(
        goals_per_game=s["gf"],
        goals_against_per_game=s["ga"],
        xGF_pct=s["xgf%"],
        corsi_for_pct=s["cf%"],
        wins=s["w"],
        losses=s["l"],
        otl=s["otl"],
        pp_pct=s["pp%"],
        pk_pct=s["pk%"]
    )
    
    return NHLTeam(
        code=code,
        name=data["name"],
        city=data["city"],
        division=data["division"],
        conference=data["conference"],
        roster=roster,
        stats=stats
    )


def load_all_teams():
    """
    Load all 32 NHL teams into the global registry.
    """
    teams = [
        # Atlantic Division - detailed loaders
        load_toronto_maple_leafs(),
        load_montreal_canadiens(),
        load_boston_bruins(),
        load_florida_panthers(),
        load_tampa_bay_lightning(),
        load_ottawa_senators(),
        load_detroit_red_wings(),
        load_buffalo_sabres(),
    ]
    
    # Load remaining teams from compact data
    from all_nhl_teams_data import ALL_TEAMS_DATA
    for code, data in ALL_TEAMS_DATA.items():
        if data is not None and code not in NHL_TEAMS:  # Skip already loaded teams
            teams.append(load_team_from_data(code, data))
    
    for team in teams:
        NHL_TEAMS[team.code] = team
    
    return len(teams)


if __name__ == "__main__":
    """Test the data loader."""
    import sys
    import io
    
    # Fix Windows encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Loading NHL team data...")
    count = load_all_teams()
    print(f"✅ Loaded {count} NHL teams\n")
    
    # Display team info
    for code, team in NHL_TEAMS.items():
        print(f"\n{'='*60}")
        print(f"{team.full_name} ({team.code})")
        print(f"{'='*60}")
        print(f"Division: {team.division} ({team.conference} Conference)")
        print(f"Record: {team.stats.wins}-{team.stats.losses}-{team.stats.otl} ({team.stats.points} pts)")
        print(f"\nOffensive Strength: {team.offensive_strength:.1f}/100")
        print(f"Defensive Strength: {team.defensive_strength:.1f}/100")
        print(f"Overall Strength: {team.overall_strength:.1f}/100")
        
        print(f"\nTop Players:")
        top_forwards = team.roster.get_top_line_forwards()
        print(f"  Forwards: {', '.join(p.name for p in top_forwards[:3])}")
        
        top_d = team.roster.get_top_defensemen()
        print(f"  Defense: {', '.join(p.name for p in top_d[:2])}")
        
        goalie = team.roster.get_starting_goalie()
        if goalie:
            print(f"  Goalie: {goalie.name} ({goalie.save_pct:.3f} SV%)")
        
        print(f"\nTeam Stats:")
        print(f"  Goals/Game: {team.stats.goals_per_game:.2f}")
        print(f"  Goals Against/Game: {team.stats.goals_against_per_game:.2f}")
        print(f"  Goal Diff: {team.stats.goal_differential:+.2f}")
        print(f"  xGF%: {team.stats.xGF_pct:.1f}%")
        print(f"  PP%: {team.stats.pp_pct:.1f}%")
        print(f"  PK%: {team.stats.pk_pct:.1f}%")

