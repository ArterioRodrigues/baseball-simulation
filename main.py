from helper import load_all_players
from simulation_game import simulate_game 
from optimize_lineup import OptimizeLineup

players_dict = load_all_players('baseballStatistics/players.csv')

mets_names = [
    "Francisco Lindor",
    "Juan Soto",
    "Pete Alonso",
    "Brandon Nimmo",
    "Starling Marte",
    "Francisco Alvarez",
    "Brett Baty",
    "Mark Vientos",
    "Tyrone Taylor"
]

yankees_names = [
    "Jazz Chisholm Jr.",
    "Aaron Judge",
    "Cody Bellinger",
    "Giancarlo Stanton",
    "Paul Goldschmidt",
    "Trent Grisham",
    "Ryan McMahon",
    "Austin Wells",
    "Anthony Volpe"
]

lineup_1_names = [
    "Juan Soto",
    "Pete Alonso",
    "Francisco Lindor",
    "Brandon Nimmo",
    "Starling Marte",
    "Brett Baty",
    "Mark Vientos",
    "Luisangel Acuña",
    "Francisco Alvarez"
]

lineup_2_names = [
    "Francisco Alvarez",
    "Luisangel Acuña",
    "Mark Vientos",
    "Brett Baty",
    "Starling Marte",
    "Brandon Nimmo",
    "Francisco Lindor",
    "Pete Alonso",
    "Juan Soto"
]


def get_lineup_from_names(names_list):
    lineup = []
    for name in names_list:
        if name in players_dict:
            lineup.append(players_dict[name])
        else:
            print(f" Warning: Player '{name}' not found in CSV!")
    return lineup

manual_lineup_1 = get_lineup_from_names(lineup_1_names)
manual_lineup_2 = get_lineup_from_names(lineup_2_names)


mets_lineup = [players_dict[name] for name in mets_names if name in players_dict]
yankees_lineup = [players_dict[name] for name in yankees_names if name in players_dict]
mets_team_code = "NYM"
yankees_team_code = "NYY"

optimizer = OptimizeLineup(manual_lineup_1, yankees_lineup, "NYM", "NYY")
optimal_lineup, win_rate = optimizer.optimize()


if len(manual_lineup_1) == 9 and len(manual_lineup_2) == 9:
    optimizer.compare_lineups(
        manual_lineup_1, 
        manual_lineup_2, 
        team_code_a="NYM", 
        team_code_b="NYM", 
        max_games=100000, 
        batch_size=1000,
        lineup_a_name="Manual Lineup 1", 
        lineup_b_name="Manual Lineup 2"
    )
else:
    print(" Error: One or both lineups do not have exactly 9 valid players.")

# In main.py

# optimizer.compare_lineups(
#     mets_lineup, 
#     optimal_lineup, 
#     mets_team_code, 
#     mets_team_code, 
#     max_games=200000, 
#     batch_size=2000, 
#     lineup_a_name="Original Mets Lineup", 
#     lineup_b_name="Optimized Mets Lineup"
# )

#if len(mets_lineup) != 9 or len(yankees_lineup) != 9:
#    print("Error: One or more players not found in CSV.")
#    print(f"Mets: {len(mets_lineup)} players")
#    print(f"Yankees: {len(yankees_lineup)} players")
#else:
#    n_games = 100000
#    mets_wins = 0
#    yankees_wins = 0
#    print(f"Simulating {n_games} games with hardcoded lineups...")
#    for i in range(n_games):
#        result = simulate_game(mets_lineup, yankees_lineup)
#        if result['NYM'] > result['NYY']:
#            mets_wins += 1
#        else:
#            yankees_wins += 1
#    print("-" * 30)
#    print(f"Final Results ({n_games} games):")
#    print(f"Mets Wins: {mets_wins}")
#    print(f"Yankees Wins: {yankees_wins}")
