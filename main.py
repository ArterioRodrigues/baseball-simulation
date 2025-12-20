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

mets_lineup = [players_dict[name] for name in mets_names if name in players_dict]
yankees_lineup = [players_dict[name] for name in yankees_names if name in players_dict]
mets_team_code = "NYM"
yankees_team_code = "NYY"

optimizer = OptimizeLineup(mets_lineup, yankees_lineup, mets_team_code, yankees_team_code)
optimal_lineup, win_rate = optimizer.optimize()

optimizer.compare_lineups( mets_lineup, optimal_lineup, mets_team_code, mets_team_code, n_games= 10000, lineup_a_name="Original Mets Lineup", lineup_b_name="Optimized Mets Lineup")
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
