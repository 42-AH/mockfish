# Mockfish
## A Minimax Chess Engine

![Mockfish1](https://github.com/42-AH/Mockfish/assets/162044943/5608db62-b128-449d-a010-fa8ca6a57051)





Mockfish is a low-level chess AI, powered by the minimax algorithm written in 100% Python.
It has an estimated 1550 ELO on hard mode, with an average accuracy of 87.9%  compared to the leading chess engine.

## MINIMAX
Minmax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case scenario.
This engine calculates every possible combination of moves up to a certain depth, and assignes each ending a score. The higher the score (or lower, depending on the turn,) the better the move. 
## MOVING
Pretty simple, just click where you want to move from to where you want to move
## Installation
```pip install mockfish```

__Or__

```
import os
os.system("pip install mockfish")
```
### Install .exe
```pyinstaller --onefile --windowed --add-data "assets;assets" main.py```
## GUI
I made a simple UI, using tkinter, so that you didn't have to put in chess notations.

## Copyright

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright (C) 2023 42-AH
