# Battleship
Battleship is a classic two person game, originally played with pen and paper.

## How to play
On a grid (typically 10 x 10), players ’hide’ ships of mixed length; horizontally or vertically (not diagonally) without any overlaps. The exact types and number of ships varies by rule, but for this posting, I’m using ships of lengths: 5, 4, 3, 3, 2 (which results in 17 possible targets out of the total of 100 squares).

## Strategy
A simple implementation of this refined strategy is to create a stack of potential targets. Initially, the computer is in Hunt mode, firing at random. Once a ship has been 'winged' then the computer switches to Target mode. After a hit, the four surrounding grid squares are added to a stack of 'potential' targets (or less than four if the cell was on an edge/corner).

Cells are only added if they have not already been visited (there is no point in re-visiting a cell if we already know that it is a Hit or Miss).

Once in Target mode the computer pops off the next potential target off the stack, fires a salvo at this location, acts on this (either adding more potential targets to the stack, or popping the next target location off the stack), until either all ships have been sunk, or there are no more potential targets on the stack, at which point it returns to Hunt mode and starts firing at random again looking for another ship.

Even though far from elegant, this algorithm produces signifincantly better results than random firing. It is, however, a long way from efficient as it has no concept of what constitutes a ship, and blindly needs to walk around all surrounding edges of every hit pixel (with the exception of the last hit one), making sure there are no more ships touching.


## Reference
http://datagenetics.com/blog/december32011/index.html
