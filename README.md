# 5x5-Go-Playing-Agent
Click [here](https://github.com/purvaingle/5x5-Go-Playing-Agent/blob/main/Problem_Statement.pdf) for the detailed problem description.

• Implemented Minimax algorithm using Alpha-beta Pruning from scratch.

• Competed against some basic as well as more advanced AI agents such as: 
- Random Player: Moves randomly.
- Greedy Player: Places the stone that captures the maximum number of enemy stones
- Aggressive Player: Looks at the next two possible moves and tries to capture the maximum number of enemy stones.
- Alpha-beta Player: Uses the Minimax algorithm (Depth<=2; Branching factor<=10) with alpha-beta pruning.
- QLearningPlayer: Uses Q-Learning to learn Q values from practice games and make moves intelligently under different game conditions.
- Championship Player: This is an excellent Little-Go player adapted from top-performing agents in previous iterations of this class.

• My agent won against the Random, Greedy, Aggressive, Alpha-beta players by winning 10 out of 10 matches with each player. Won 5 matches against the Q-Learning player and 2 matches against the Championship player.
