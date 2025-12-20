import random
from player import Player
from typing import List, Optional, Tuple
from simulation_game import simulate_game

PLAYER_TEAM_CODE = "NYM"
OPPONENT_TEAM_CODE = "NYY"

class OptimizeLineup:
    def __init__(self, players_lineup: List[Player], opponents_lineup: List[Player], player_team_code: str = PLAYER_TEAM_CODE, opponent_team_code: str = OPPONENT_TEAM_CODE):
        self.players_lineup = players_lineup
        self.opponents_lineup = opponents_lineup

        self.player_team_code = player_team_code
        self.opponent_team_code = opponent_team_code

        self.best_lineup = [] 
        self.best_fitness = 0 

        self.generation_history = []
       

    def create_random_lineup(self, team_code: str = PLAYER_TEAM_CODE) -> List[Player]: 
        lineup = self.players_lineup if self.player_team_code == team_code else self.opponents_lineup
        return random.sample(lineup, len(lineup)) 

    def evaluate_fitness(self, lineup: List[Player], team_code: str, n_games: int = 1000) -> float:
        wins = 0
        for _ in range(n_games): 
            if(team_code == self.player_team_code): 
                result = simulate_game(lineup, self.opponents_lineup, team_code, self.opponent_team_code);
                if result[self.player_team_code] > result[self.opponent_team_code]:
                    wins += 1
            else:
                result = simulate_game(self.players_lineup, lineup, self.player_team_code, team_code);
                if result[self.opponent_team_code] > result[self.player_team_code]:
                    wins += 1

        return wins/n_games

    def tournament_selection(self, population: List[List[Player]], fitness_scores: List[float], tournament_size: int = 3) -> List[Player]:
        tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])
        return winner[0]


    def crossover(self, parent1: List[Player], parent2: List[Player]) -> List[Player]:
        size = len(parent1)
        
        start, end = sorted(random.sample(range(size), 2))
        
        child: List[Optional[Player]]= [None] * size
        child[start:end] = parent1[start:end]
        
        parent2_filtered = [p for p in parent2 if p not in child]
        
        idx = 0
        for i in range(size):
            if child[i] is None:
                child[i] = parent2_filtered[idx]
                idx += 1
        child_players: List[Player] = [p for p in child if p is not None]
        return child_players

    def mutate(self, lineup: List[Player], mutation_rate: float = 0.2) -> List[Player]:
        if random.random() < mutation_rate:
            mutated = lineup.copy()
            
            idx1, idx2 = random.sample(range(len(mutated)), 2)
            mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
            
            return mutated
        
        return lineup

    def compare_lineups(self, lineup_a: List[Player], lineup_b: List[Player], team_code_a: str, team_code_b: str, n_games: int = 10000, lineup_a_name: str = "Lineup A", lineup_b_name: str = "Lineup B") -> dict:
        
        fitness_a = self.evaluate_fitness(lineup_a, team_code_a, n_games)
        fitness_b = self.evaluate_fitness(lineup_b, team_code_b, n_games)
        
        improvement = ((fitness_b - fitness_a) / fitness_a * 100) if fitness_a > 0 else 0
        
        print(f"\n{lineup_a_name}:")
        for i, player in enumerate(lineup_a, 1):
            print(f"  {i}. {player.name}")
        print(f"  Win Rate: {fitness_a:.3f} ({fitness_a*100:.1f}%)")
        
        print(f"\n{lineup_b_name}:")
        for i, player in enumerate(lineup_b, 1):
            print(f"  {i}. {player.name}")
        print(f"  Win Rate: {fitness_b:.3f} ({fitness_b*100:.1f}%)")
        
        print(f"\n📊 Results:")
        print(f"  Improvement: {improvement:+.2f}%")
        
        if fitness_b > fitness_a:
            print(f"  🎉 {lineup_b_name} is better!")
        elif fitness_b < fitness_a:
            print(f"  {lineup_a_name} is better!")
        else:
            print(f"  Both lineups perform equally")
        
        return {
            'lineup_a_win_rate': fitness_a,
            'lineup_b_win_rate': fitness_b,
            'improvement_pct': improvement,
            'winner': lineup_b_name if fitness_b > fitness_a else lineup_a_name
        }
    
    def optimize(self, team_code: str = PLAYER_TEAM_CODE, population_size: int = 50, elite_size: int = 5, mutation_rate: float = 0.2, generations: int = 30) -> Tuple[List[Player], float]:
        population = [self.create_random_lineup(team_code) for _ in range(population_size)] 
       
        for generation in range(generations):
            fitness_scores = []
            for lineup in population:
                fitness = self.evaluate_fitness(lineup, team_code)
                fitness_scores.append(fitness)
    
            best_fitness_idx = fitness_scores.index(max(fitness_scores))
            best_fitness = fitness_scores[best_fitness_idx]
            best_lineup = population[best_fitness_idx]
    
            if(best_fitness > self.best_fitness):
                self.best_fitness = best_fitness
                self.best_lineups = best_lineup
    
            self.generation_history.append({
                'generation': generation + 1,
                'best_fitness': best_fitness,
                'avg_fitness': sum(fitness_scores) / len(fitness_scores),
                'best_lineup': [p.name for p in best_lineup]
            })
    
            new_population = []
            sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
            new_population.extend(sorted_population[:elite_size])
            
            for _ in range(population_size - elite_size): 
                parent1 = self.tournament_selection(population, fitness_scores)
                parent2 = self.tournament_selection(population, fitness_scores)
                
                child = self.crossover(parent1, parent2)
                child = self.mutate(child, mutation_rate)
    
            population = new_population
        
        lineup: List[Player] = [p for p in self.best_lineup if p is not None]
        return lineup, self.best_fitness
