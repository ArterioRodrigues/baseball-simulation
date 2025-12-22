import random
import math
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

    def evaluate_fitness(self, lineup: List[Player], team_code: str, n_games: int = 1000, game_seeds: List[int] = None) -> float:
        wins = 0


        iterations = game_seeds if game_seeds is not None else range(n_games)
        
        for i in iterations:
            seed = i if game_seeds is not None else None
            
            if(team_code == self.player_team_code): 
                result = simulate_game(lineup, self.opponents_lineup, team_code, self.opponent_team_code, seed=seed)
                if result[self.player_team_code] > result[self.opponent_team_code]:
                    wins += 1
            else:
                result = simulate_game(self.players_lineup, lineup, self.player_team_code, team_code, seed=seed)
                if result[self.opponent_team_code] > result[self.player_team_code]:
                    wins += 1
        
        count = len(game_seeds) if game_seeds is not None else n_games
        return wins / count
    

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

    def compare_lineups(self, lineup_a: List[Player], lineup_b: List[Player], team_code_a: str, team_code_b: str, max_games: int = 100000, batch_size: int = 1000, lineup_a_name: str = "Lineup A", lineup_b_name: str = "Lineup B") -> dict:    
        
        
        wins_a = 0
        wins_b = 0
        current_games = 0
        
        print(f"\nComparing lineups (Checking significance every {batch_size} games up to {max_games})...")

        while current_games < max_games:

            batch_seeds = [random.randint(0, 1000000000) for _ in range(batch_size)]
            rate_a = self.evaluate_fitness(lineup_a, team_code_a, game_seeds=batch_seeds)
            rate_b = self.evaluate_fitness(lineup_b, team_code_b, game_seeds=batch_seeds)
            wins_a += rate_a * batch_size
            wins_b += rate_b * batch_size
            current_games += batch_size
            
            fitness_a = wins_a / current_games
            fitness_b = wins_b / current_games
            
            se_diff = math.sqrt( (fitness_a * (1 - fitness_a) / current_games) + (fitness_b * (1 - fitness_b) / current_games) )
            moe_diff = 1.96 * se_diff 
            
            diff = fitness_b - fitness_a
            
            if abs(diff) > moe_diff and current_games >= 5000:
                print(f"   Stopping early at {current_games} games: Statistically significant difference found.")
                break
            
            if current_games % 10000 == 0:
                print(f"  ... {current_games} games played. Current diff: {diff*100:.2f}% (MoE: ±{moe_diff*100:.2f}%)")
        se_a = math.sqrt((fitness_a * (1 - fitness_a)) / current_games) 
        moe_a = 1.96 * se_a
        
        se_b = math.sqrt((fitness_b * (1 - fitness_b)) / current_games)
        moe_b = 1.96 * se_b

        improvement = ((fitness_b - fitness_a) / fitness_a * 100) if fitness_a > 0 else 0
        

        print(f"\n{lineup_a_name}:")
        for i, player in enumerate(lineup_a, 1):
            print(f"  {i}. {player.name}")
        print(f"  Win Rate: {fitness_a:.3f} ± {moe_a:.3f} (95% CI: [{fitness_a - moe_a:.3f}, {fitness_a + moe_a:.3f}])")
        
        print(f"\n{lineup_b_name}:")
        for i, player in enumerate(lineup_b, 1):
            print(f"  {i}. {player.name}")
        print(f"  Win Rate: {fitness_b:.3f} ± {moe_b:.3f} (95% CI: [{fitness_b - moe_b:.3f}, {fitness_b + moe_b:.3f}])")
        
        print(f"\nResults:")
        print(f"  Improvement: {improvement:+.2f}%")
        
        se_diff = math.sqrt( (fitness_a * (1 - fitness_a) / current_games) + (fitness_b * (1 - fitness_b) / current_games) )
        moe_diff = 1.96 * se_diff
        diff = fitness_b - fitness_a
        
        print(f"  Difference: {diff:.3f} ± {moe_diff:.3f}")
        
        if abs(diff) > moe_diff:
            if diff > 0:
                print(f"  {lineup_b_name} is statistically significantly better!")
            else:
                print(f"  {lineup_a_name} is statistically significantly better!")
        else:
            print(f"  The difference is not statistically significant (within margin of error).")
        
        return {
            'lineup_a_win_rate': fitness_a,
            'lineup_b_win_rate': fitness_b,
            'improvement_pct': improvement,
            'winner': lineup_b_name if fitness_b > fitness_a else lineup_a_name,
            'statistically_significant': abs(diff) > moe_diff
        }
    
    def optimize(self, team_code: str = PLAYER_TEAM_CODE, population_size: int = 50, elite_size: int = 5, mutation_rate: float = 0.2, generations: int = 50) -> Tuple[List[Player], float]:
        population = [self.create_random_lineup(team_code) for _ in range(population_size)] 
        
        games_per_eval = 3000 
       
        for generation in range(generations):
            generation_seeds = [random.randint(0, 1000000000) for _ in range(games_per_eval)]
            
            fitness_scores = []
            for lineup in population:
                fitness = self.evaluate_fitness(lineup, team_code, game_seeds=generation_seeds)
                fitness_scores.append(fitness)
    
            best_fitness_idx = fitness_scores.index(max(fitness_scores))
            best_fitness = fitness_scores[best_fitness_idx]
            best_lineup = population[best_fitness_idx]
    
            if(best_fitness > self.best_fitness):
                self.best_fitness = best_fitness
                self.best_lineup = best_lineup
    
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
                new_population.append(child)
    
            population = new_population
        
        lineup: List[Player] = [p for p in self.best_lineup if p is not None]
        return lineup, self.best_fitness
