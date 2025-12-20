import csv
from player import Player

def load_all_players(filename):
    players = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                players[row['Name']] = Player(row)
    except Exception as e:
        print(f"Error reading file: {e}")
    return players
