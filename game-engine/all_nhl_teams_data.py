"""
Compact NHL Team Data for All 32 Teams

This contains team stats and top players for efficient loading.
"""

# Format: (code, name, city, division, conference, top_players, team_stats)
# top_players: [(name, position, number, rating), ...]
# team_stats: {gf, ga, xgf%, corsi%, w, l, otl, pp%, pk%}

ALL_TEAMS_DATA = {
    # Atlantic Division (already loaded in detail)
    "TOR": None,  # Skip - already loaded
    "MTL": None,
    "BOS": None,
    "FLA": None,
    "TBL": None,
    "OTT": None,
    "DET": None,
    "BUF": None,
    
    # Metropolitan Division
    "NYR": {
        "name": "Rangers", "city": "New York", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Artemi Panarin", "LW", 10, 94), ("Mika Zibanejad", "C", 93, 88), ("Adam Fox", "D", 23, 94),
            ("Chris Kreider", "LW", 20, 86), ("Vincent Trocheck", "C", 16, 84), ("K'Andre Miller", "D", 79, 84),
            ("Igor Shesterkin", "G", 31, 95), ("Alexis Lafrenière", "RW", 13, 85)
        ],
        "stats": {"gf": 3.4, "ga": 2.7, "xgf%": 53.5, "cf%": 52.0, "w": 11, "l": 4, "otl": 1, "pp%": 22.5, "pk%": 84.0}
    },
    
    "CAR": {
        "name": "Hurricanes", "city": "Carolina", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Sebastian Aho", "C", 20, 92), ("Andrei Svechnikov", "LW", 37, 89), ("Martin Necas", "RW", 88, 86),
            ("Jaccob Slavin", "D", 74, 91), ("Brent Burns", "D", 8, 85), ("Frederik Andersen", "G", 31, 85)
        ],
        "stats": {"gf": 3.3, "ga": 2.6, "xgf%": 55.0, "cf%": 54.0, "w": 10, "l": 5, "otl": 0, "pp%": 21.0, "pk%": 85.0}
    },
    
    "NJD": {
        "name": "Devils", "city": "New Jersey", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Jack Hughes", "C", 86, 93), ("Nico Hischier", "C", 13, 89), ("Jesper Bratt", "RW", 63, 87),
            ("Dougie Hamilton", "D", 7, 88), ("Timo Meier", "LW", 96, 85), ("Jacob Markström", "G", 25, 86)
        ],
        "stats": {"gf": 3.2, "ga": 3.0, "xgf%": 52.0, "cf%": 51.0, "w": 9, "l": 7, "otl": 1, "pp%": 23.0, "pk%": 80.0}
    },
    
    "NYI": {
        "name": "Islanders", "city": "New York", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Mathew Barzal", "C", 13, 88), ("Bo Horvat", "C", 14, 84), ("Brock Nelson", "C", 29, 82),
            ("Noah Dobson", "D", 8, 84), ("Adam Pelech", "D", 3, 82), ("Ilya Sorokin", "G", 30, 89)
        ],
        "stats": {"gf": 2.9, "ga": 2.9, "xgf%": 49.5, "cf%": 49.0, "w": 7, "l": 7, "otl": 3, "pp%": 19.5, "pk%": 81.5}
    },
    
    "PHI": {
        "name": "Flyers", "city": "Philadelphia", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Travis Konecny", "RW", 11, 86), ("Sean Couturier", "C", 14, 83), ("Owen Tippett", "RW", 74, 80),
            ("Cam York", "D", 59, 81), ("Travis Sanheim", "D", 6, 80), ("Samuel Ersson", "G", 33, 79)
        ],
        "stats": {"gf": 2.8, "ga": 3.3, "xgf%": 47.0, "cf%": 47.5, "w": 6, "l": 9, "otl": 2, "pp%": 18.5, "pk%": 77.0}
    },
    
    "PIT": {
        "name": "Penguins", "city": "Pittsburgh", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Sidney Crosby", "C", 87, 91), ("Evgeni Malkin", "C", 71, 85), ("Erik Karlsson", "D", 65, 87),
            ("Bryan Rust", "RW", 17, 84), ("Rickard Rakell", "C", 67, 81), ("Tristan Jarry", "G", 35, 80)
        ],
        "stats": {"gf": 2.9, "ga": 3.4, "xgf%": 48.0, "cf%": 48.5, "w": 6, "l": 9, "otl": 2, "pp%": 19.0, "pk%": 76.5}
    },
    
    "WSH": {
        "name": "Capitals", "city": "Washington", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Alex Ovechkin", "LW", 8, 89), ("Dylan Strome", "C", 17, 84), ("Tom Wilson", "RW", 43, 83),
            ("John Carlson", "D", 74, 84), ("Jakob Chychrun", "D", 6, 82), ("Charlie Lindgren", "G", 79, 83)
        ],
        "stats": {"gf": 3.1, "ga": 3.1, "xgf%": 49.0, "cf%": 49.5, "w": 8, "l": 6, "otl": 1, "pp%": 20.5, "pk%": 79.0}
    },
    
    "CBJ": {
        "name": "Blue Jackets", "city": "Columbus", "division": "Metropolitan", "conference": "Eastern",
        "players": [
            ("Johnny Gaudreau", "LW", 13, 87), ("Sean Monahan", "C", 91, 81), ("Patrik Laine", "RW", 29, 84),
            ("Zach Werenski", "D", 8, 87), ("Ivan Provorov", "D", 47, 79), ("Elvis Merzlikins", "G", 90, 78)
        ],
        "stats": {"gf": 2.7, "ga": 3.7, "xgf%": 45.5, "cf%": 46.0, "w": 5, "l": 9, "otl": 2, "pp%": 17.0, "pk%": 74.0}
    },
    
    # Central Division
    "COL": {
        "name": "Avalanche", "city": "Colorado", "division": "Central", "conference": "Western",
        "players": [
            ("Nathan MacKinnon", "C", 29, 97), ("Cale Makar", "D", 8, 96), ("Mikko Rantanen", "RW", 96, 92),
            ("Valeri Nichushkin", "RW", 13, 85), ("Devon Toews", "D", 7, 87), ("Alexandar Georgiev", "G", 40, 81)
        ],
        "stats": {"gf": 3.6, "ga": 2.9, "xgf%": 54.5, "cf%": 53.5, "w": 10, "l": 7, "otl": 0, "pp%": 24.0, "pk%": 82.5}
    },
    
    "DAL": {
        "name": "Stars", "city": "Dallas", "division": "Central", "conference": "Western",
        "players": [
            ("Jason Robertson", "LW", 21, 91), ("Roope Hintz", "C", 24, 88), ("Tyler Seguin", "C", 91, 84),
            ("Miro Heiskanen", "D", 4, 91), ("Esa Lindell", "D", 23, 83), ("Jake Oettinger", "G", 29, 90)
        ],
        "stats": {"gf": 3.3, "ga": 2.7, "xgf%": 53.0, "cf%": 52.5, "w": 10, "l": 6, "otl": 0, "pp%": 22.0, "pk%": 83.5}
    },
    
    "WPG": {
        "name": "Jets", "city": "Winnipeg", "division": "Central", "conference": "Western",
        "players": [
            ("Mark Scheifele", "C", 55, 88), ("Kyle Connor", "LW", 81, 90), ("Nikolaj Ehlers", "LW", 27, 85),
            ("Josh Morrissey", "D", 44, 87), ("Neal Pionk", "D", 4, 80), ("Connor Hellebuyck", "G", 37, 93)
        ],
        "stats": {"gf": 3.4, "ga": 2.6, "xgf%": 54.0, "cf%": 53.0, "w": 12, "l": 3, "otl": 0, "pp%": 25.0, "pk%": 84.5}
    },
    
    "MIN": {
        "name": "Wild", "city": "Minnesota", "division": "Central", "conference": "Western",
        "players": [
            ("Kirill Kaprizov", "LW", 97, 94), ("Matt Boldy", "LW", 12, 86), ("Joel Eriksson Ek", "C", 14, 84),
            ("Jared Spurgeon", "D", 46, 83), ("Jonas Brodin", "D", 25, 82), ("Filip Gustavsson", "G", 32, 84)
        ],
        "stats": {"gf": 3.1, "ga": 2.9, "xgf%": 51.0, "cf%": 50.5, "w": 8, "l": 6, "otl": 2, "pp%": 21.5, "pk%": 81.0}
    },
    
    "NSH": {
        "name": "Predators", "city": "Nashville", "division": "Central", "conference": "Western",
        "players": [
            ("Filip Forsberg", "LW", 9, 88), ("Roman Josi", "D", 59, 91), ("Ryan O'Reilly", "C", 90, 83),
            ("Gustav Nyquist", "RW", 14, 81), ("Alexandre Carrier", "D", 45, 79), ("Juuse Saros", "G", 74, 89)
        ],
        "stats": {"gf": 2.9, "ga": 3.2, "xgf%": 48.5, "cf%": 48.0, "w": 6, "l": 9, "otl": 1, "pp%": 19.5, "pk%": 78.5}
    },
    
    "STL": {
        "name": "Blues", "city": "St. Louis", "division": "Central", "conference": "Western",
        "players": [
            ("Robert Thomas", "C", 18, 86), ("Jordan Kyrou", "RW", 25, 85), ("Pavel Buchnevich", "RW", 89, 84),
            ("Colton Parayko", "D", 55, 82), ("Torey Krug", "D", 47, 81), ("Jordan Binnington", "G", 50, 81)
        ],
        "stats": {"gf": 2.9, "ga": 3.3, "xgf%": 48.0, "cf%": 47.5, "w": 7, "l": 9, "otl": 0, "pp%": 18.0, "pk%": 77.5}
    },
    
    "UTA": {
        "name": "Hockey Club", "city": "Utah", "division": "Central", "conference": "Western",
        "players": [
            ("Clayton Keller", "C", 9, 87), ("Nick Schmaltz", "C", 8, 82), ("Logan Cooley", "C", 92, 80),
            ("Mikhail Sergachev", "D", 98, 85), ("J.J. Moser", "D", 14, 78), ("Karel Vejmelka", "G", 70, 77)
        ],
        "stats": {"gf": 2.7, "ga": 3.6, "xgf%": 46.0, "cf%": 46.5, "w": 6, "l": 9, "otl": 2, "pp%": 17.5, "pk%": 75.5}
    },
    
    "CHI": {
        "name": "Blackhawks", "city": "Chicago", "division": "Central", "conference": "Western",
        "players": [
            ("Connor Bedard", "C", 98, 91), ("Tyler Bertuzzi", "LW", 59, 82), ("Taylor Hall", "LW", 71, 81),
            ("Seth Jones", "D", 4, 82), ("Alex Vlasic", "D", 43, 78), ("Petr Mrazek", "G", 34, 79)
        ],
        "stats": {"gf": 2.6, "ga": 3.5, "xgf%": 45.0, "cf%": 45.5, "w": 6, "l": 10, "otl": 1, "pp%": 16.5, "pk%": 75.0}
    },
    
    # Pacific Division
    "VGK": {
        "name": "Golden Knights", "city": "Vegas", "division": "Pacific", "conference": "Western",
        "players": [
            ("Jack Eichel", "C", 9, 92), ("Mark Stone", "RW", 61, 90), ("Ivan Barbashev", "C", 49, 83),
            ("Alex Pietrangelo", "D", 7, 87), ("Shea Theodore", "D", 27, 86), ("Adin Hill", "G", 33, 84)
        ],
        "stats": {"gf": 3.4, "ga": 2.9, "xgf%": 52.5, "cf%": 52.0, "w": 10, "l": 5, "otl": 2, "pp%": 23.5, "pk%": 82.0}
    },
    
    "EDM": {
        "name": "Oilers", "city": "Edmonton", "division": "Pacific", "conference": "Western",
        "players": [
            ("Connor McDavid", "C", 97, 99), ("Leon Draisaitl", "C", 29, 95), ("Ryan Nugent-Hopkins", "C", 93, 87),
            ("Evan Bouchard", "D", 2, 89), ("Mattias Ekholm", "D", 14, 84), ("Stuart Skinner", "G", 74, 83)
        ],
        "stats": {"gf": 3.6, "ga": 2.9, "xgf%": 54.0, "cf%": 53.0, "w": 10, "l": 7, "otl": 0, "pp%": 27.0, "pk%": 81.5}
    },
    
    "LAK": {
        "name": "Kings", "city": "Los Angeles", "division": "Pacific", "conference": "Western",
        "players": [
            ("Anze Kopitar", "C", 11, 88), ("Adrian Kempe", "C", 9, 86), ("Quinton Byfield", "C", 55, 83),
            ("Drew Doughty", "D", 8, 86), ("Mikey Anderson", "D", 44, 80), ("Darcy Kuemper", "G", 35, 82)
        ],
        "stats": {"gf": 3.0, "ga": 2.9, "xgf%": 50.5, "cf%": 50.0, "w": 8, "l": 6, "otl": 2, "pp%": 20.5, "pk%": 81.0}
    },
    
    "VAN": {
        "name": "Canucks", "city": "Vancouver", "division": "Pacific", "conference": "Western",
        "players": [
            ("Elias Pettersson", "C", 40, 91), ("J.T. Miller", "C", 9, 89), ("Brock Boeser", "RW", 6, 85),
            ("Quinn Hughes", "D", 43, 94), ("Filip Hronek", "D", 17, 82), ("Thatcher Demko", "G", 35, 88)
        ],
        "stats": {"gf": 3.2, "ga": 2.8, "xgf%": 52.0, "cf%": 51.5, "w": 9, "l": 6, "otl": 2, "pp%": 22.5, "pk%": 82.5}
    },
    
    "SEA": {
        "name": "Kraken", "city": "Seattle", "division": "Pacific", "conference": "Western",
        "players": [
            ("Jared McCann", "C", 19, 84), ("Matty Beniers", "C", 10, 81), ("Jordan Eberle", "RW", 7, 82),
            ("Vince Dunn", "D", 29, 83), ("Adam Larsson", "D", 6, 79), ("Philipp Grubauer", "G", 31, 80)
        ],
        "stats": {"gf": 2.9, "ga": 3.1, "xgf%": 49.0, "cf%": 48.5, "w": 8, "l": 8, "otl": 1, "pp%": 19.0, "pk%": 79.0}
    },
    
    "CGY": {
        "name": "Flames", "city": "Calgary", "division": "Pacific", "conference": "Western",
        "players": [
            ("Jonathan Huberdeau", "LW", 10, 85), ("Nazem Kadri", "C", 91, 83), ("Andrei Kuzmenko", "LW", 96, 82),
            ("Rasmus Andersson", "D", 4, 84), ("MacKenzie Weegar", "D", 52, 82), ("Dan Vladar", "G", 80, 79)
        ],
        "stats": {"gf": 2.8, "ga": 3.3, "xgf%": 47.5, "cf%": 47.0, "w": 7, "l": 8, "otl": 2, "pp%": 18.5, "pk%": 77.5}
    },
    
    "ANA": {
        "name": "Ducks", "city": "Anaheim", "division": "Pacific", "conference": "Western",
        "players": [
            ("Trevor Zegras", "C", 46, 84), ("Mason McTavish", "C", 37, 81), ("Frank Vatrano", "RW", 77, 80),
            ("Cam Fowler", "D", 4, 81), ("Radko Gudas", "D", 7, 77), ("John Gibson", "G", 36, 80)
        ],
        "stats": {"gf": 2.6, "ga": 3.6, "xgf%": 45.5, "cf%": 45.0, "w": 5, "l": 10, "otl": 2, "pp%": 16.0, "pk%": 74.5}
    },
    
    "SJS": {
        "name": "Sharks", "city": "San Jose", "division": "Pacific", "conference": "Western",
        "players": [
            ("Will Smith", "C", 2, 86), ("Macklin Celebrini", "C", 71, 88), ("Mikael Granlund", "C", 64, 81),
            ("Jake Walman", "D", 24, 79), ("Cody Ceci", "D", 4, 75), ("Mackenzie Blackwood", "G", 29, 78)
        ],
        "stats": {"gf": 2.5, "ga": 3.8, "xgf%": 44.0, "cf%": 44.5, "w": 5, "l": 11, "otl": 1, "pp%": 15.5, "pk%": 73.0}
    },
}



