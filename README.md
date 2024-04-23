# Mockfish
## A minimax chess engine
### https://replit.com/@42AH/Mockfish-A-minimax-chess-engine

![Mockfish1](https://github.com/42-AH/Mockfish/assets/162044943/5608db62-b128-449d-a010-fa8ca6a57051)





Mockfish is a low-level chess AI, powered by the minimax algorithm, using alpha-beta pruning, created by 42-AH.

## MINIMAX
Minmax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case scenario.
This engine calculates every possible combination of moves up to a certain depth, and assignes each ending a score. The higher the score (or lower, depending on the turn,) the better the move. 

## MOVEMENT
Type the square your moving from, and the square your moving to, no spaces.
Examples:
e2e4
g1f3

Board:
```
Move: e2e4 
WHITE
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
 
BLACK
Score: 75
r . b q k b n r
p p p p p p p p
. . n . . . . .
. . . . . . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
 
Move: g1f3
WHITE
r . b q k b n r
p p p p p p p p
. . n . . . . .
. . . . . . . .
. . . . P . . .
. . . . . N . .
P P P P . P P P
R N B Q K B . R
 
BLACK
Score: 75
r . b q k b . r
p p p p p p p p
. . n . . n . .
. . . . . . . .
. . . . P . . .
. . . . . N . .
P P P P . P P P
R N B Q K B . R
```
### ELO
Depth 3 has an estimated 2000 ELO
Depth 4 has much more, but is too slow (at least on my current setup,) for me to spend the time to get an estimate.


## Copyright
Copyright (C) 2023 42-AH

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.






Copyright (C) 2023 42-AH
