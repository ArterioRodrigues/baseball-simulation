import random
from player import Player
from helper import load_all_players


def simulate_game(players_lineup, opponents_lineup, player_team_code, opponent_team_code):
    inning = 1
    top_of_inning = True
    bases = [False, False, False]
    outs = 0
    score = {player_team_code: 0, opponent_team_code: 0}

    player_idx = 0
    opponent_idx = 0

    while True:
        if top_of_inning:
            batter = players_lineup[player_idx]
            player_idx = (player_idx + 1) % 9
            batting_team = player_team_code
        else:
            batter = opponents_lineup[opponent_idx]
            opponent_idx = (opponent_idx + 1) % 9
            batting_team = opponent_team_code

        events = list(batter.probs.keys())
        weights = list(batter.probs.values())
        event = random.choices(events, weights=weights, k=1)[0]

        if event == 'out':
            outs += 1
        elif event == 'walk':
            if bases[0] and bases[1] and bases[2]:
                score[batting_team] += 1
            elif bases[0] and bases[1]:
                bases[2] = True
            elif bases[0]: 
                bases[1] = True

        elif event == 'single':
            if bases[2]: score[batting_team] += 1; bases[2] = False
            if bases[1]: bases[2] = True; bases[1] = False
            if bases[0]: bases[1] = True; bases[0] = False
            bases[0] = True
        elif event == 'double':
            if bases[2]: score[batting_team] += 1; bases[2] = False
            if bases[1]: score[batting_team] += 1; bases[1] = False
            if bases[0]: bases[2] = True; bases[0] = False
            bases[1] = True
        elif event == 'triple':
            runs = sum(bases)
            score[batting_team] += runs
            bases = [False, False, False]
            bases[2] = True
        elif event == 'hr':
            runs = sum(bases) + 1
            score[batting_team] += runs
            bases = [False, False, False]

        if outs >= 3:
            outs = 0
            bases = [False, False, False]
            if top_of_inning:
                top_of_inning = False
            else:
                top_of_inning = True
                inning += 1

        if inning > 9 and top_of_inning:
            if score['NYM'] != score['NYY']:
                break
        if inning >= 9 and not top_of_inning and score['NYY'] > score['NYM']:
            break

    return score
