#**Quoridor**
___
This version of Quoridor is the first game I built using Python and pygame. The backend code was initially a final
project from my introductory CS classes. After the classes have ended, I have added the UI using pygame. Features are still
being added to this game. 

##Required
___
Python 3, pygame

##Rules
___
**What is the objective of Quoridor?** The first player to reach any square on the opponent's baseline wins the game.

**What is a turn?**
A player can either (1) place a fence horizontally or vertically or (2) move a pawn orthogonally (non-diagonal) one space. The first player to take a turn during the game is player 1 (red square) and then rotates to player 2 (blue square) and then back to player 1 and so on.

**What happens when I place a fence?**
Each player has 10 fences that can be placed on the board to blocks all players from moving over this fence. A fence is one block long in this version of the game and only one fence can be placed at a time during a turn.

**What happens if the pawns are next to each other?**

Scenario 1: No fences around players
- Pawns cannot move to the same square as another pawn.
- The jump move: The moving pawn may jump over the opposing pawn

Scenario 2: There is a fence behind, or around, the opposingpawn.
- Pawns cannot move to the same square as another pawn.
- The moving pawn can't jump over the opposing pawn because there is a fence behind the opposing pawn, but the moving pawn can may move diagonally.
- In general, the moving pawn may move to all squares that the opposing pawn may move to.
