# Baseball-Simulation

Baseball simulation is developed by Group 2 and simulates the outcome of the MLB team matchups.

## Motivation
- Baseball is unpredictable; simulations can model thousands of possible outcomes to capture real performance variability.
- Leveraging the Monte Carlo method would aid in optimizing pitch-batter splits and lineup interactions to find the lineup with the highest win probability.
- Turns lineups driven by intuition into evidence-backed strategy by showing which players consistently improve expected runs and win rates.

## Simulaton Model
- DTMC: The previous game states (filtration) will have no effect on the current state of our simulation.
    - We will track the current game state (outs, players on base, current inning, current hitter, current pitcher). 
    - We get our player and team data from [baseball-reference](https://www.baseball-reference.com). 
    - The outcome of a plate appearance will be determined by a simple categorical distribution. (eg. X player hits a home run Y% of the time against Z pitcher).

## Goal
We want to determine if a team’s chance of winning will increase or not depending on if a player is switched out.

## Future Implications
- Developing the model with more data and complex variance control methods can improve lineup decisions and matchup-specific win probabilities
- We could further develop these into live tools to guide choices mid-game, such as defensive shifts, and pinch hitting.
- Enhanced simulation frameworks can support season-long planning, trade decisions, and player valuation, and can be generalized to other sports industries such as the NBA or the NFL.