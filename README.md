# Mockfish
## A Minimax Chess Engine

![Mockfish1](https://github.com/42-AH/Mockfish/assets/162044943/5608db62-b128-449d-a010-fa8ca6a57051)





Mockfish is a low-level chess AI, powered by the minimax algorithm written in 100% Python.
It has an estimated 1550 ELO on hard mode, with an average of 87.9% accuracy compared to the leading chess engine.

Minimax contains:
Alpha-beta pruning
Multi-threading


## MINIMAX
Minmax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case scenario.
This engine calculates every possible combination of moves up to a certain depth, and assignes each ending a score. The higher the score (or lower, depending on the turn,) the better the move. 
## MOVING
Pretty simple, just click where you want to move from to where you want to move
## DOWNLOADING
### Install Git
Install Git from here: https://git-scm.com/downloads
### Clone the Repository
```git clone <https://github.com/42-AH/Mockfish>```
### Navigate to the Repository Directory
```cd <Mockfish>```
### Install Dependencies
```pip install -r requirements.txt```
### Install .exe
```pyinstaller --onefile --windowed --add-data "assets;assets" main.py```
## GUI
I made a simple UI, using tkinter, so that you didn't have to put in chess notations.

## Copyright

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

The GNU General Public License (GNU GPL) essentially allows users to buy, sell, or utilize software in any way they see fit, as long as they provide access to the corresponding source code when distributing it.

Copyright (C) 2023 42-AH
