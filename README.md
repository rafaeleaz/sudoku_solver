# sudoku_solver
This project was created with the idea of creating an algorithm in Python which solves Sudoku puzzles (and in particular, those puzzles published daily by the New York Times on their website) in the same way that humans would (or at least how I do it). This is done by filling in a number in pen only when we are certain that our answer is correct.

To solve Sudokus, I use a three step approach which has not failed me in solving the daily New York Times hard difficulty puzzles for a few months. Before I continue, however, I must confess that I have not read any books on Sudoku solving, nor am I an expert. This means that there may be valid methods of solving Sudokus of which I do not know. Furthermore, the notation I will use is by no means standard. Having said this, here are my steps:

To begin, let us first define some notation. A puzzle is made up of a grid, called a board, of 9x9 tiles, each of which is either blank or contains a single digit from 1-9. The board is then subdivided into nine rows (horizontal lines of tiles), nine columns (vertical lines of tiles), and nine disjoint 3x3 squares of tiles. When a tile contains a number, we will say that it is answered, and its corresponding number will be its answer. 

In our Python files, a board will be formatted as a list of lists, usually named simply "board". Here, board[i][j] will represent the tile in the i-th row and j-th column, and will be set to one of the strings "." or "n", where n is an integer between 1 and 9, inclusive.

We say that a board is solved when each tile is answered, such that no row, column, or square contains two tiles with identical answers. We will call tiles which share a row, column, or square row-mates, column-mates, or square-mates, respectively. We say that two tiles are mates when they share any of the three. We say that two mates conflict when they have the same answer, in which case we will say that the corresponding row, column, and/or square is in conflict.

The pencil marks are list of numbers corresponding to each unanswered tile which lists the answers which can be written into the tile withouth immediately creating a conflict on the board (notably, the pencil marks change as tiles become answered).

In our files, the pencil marks, usually named "marks", will be a list of list of lists, where marks[i][j] will be the list of all possible answers which the tile (i, j) could be without creating conflicts on the current board, where each entry is "n", with n being an integer between 1 and 9, inclusive.

Knowing these preliminaries, let us list the steps which we can follow to solve a given board (given that a solution exists, and that it is unique!)

1. Populate the pencil marks.

2. For each row, column and square, check if there is a tile which has only one pencil mark. This mark must be the tile's answer. Answer the tile with the corresponding number and adjust the pencil marks of its mates.

3. For each row, column and square, check if there is a number which appears in exactly one of its tiles pencil marks. This tile's answer must be that mark. Answer the tile with the corresponding number and adjust the pencil marks of its mates.

4. Repeat steps 2-3 until either the puzzle is solved or neither can produce a new answer. Note: steps 1-4 are enough to solve most easy puzzles.

5. In each row, column and square, and for each n with 2 <= n <= 4, check if there are n tiles whose pencil marks form a set A, say, of exactly n numbers. This implies that none of the other tiles therein may be answered with numbers belonging to A. Now delete all members of A from the pencil marks of the tiles which are not in our list of n which we used to form A.

6. Repeat steps 2-5 until either the puzzle is solved or none of them can produce a new answer or eliminate pencil marks.

And that's it (hopefully)! If this algorithm cannot solve a certain puzzle, then it would also stump me :( Furthermore, any puzzle solved by this method is guaranteed to have a unique answer! This is because we only ever make a move if there is no possible way that the move is incorrect. Therefore, this also works as a (perhaps somewhat rudimentary) way of checking that a puzzle has a unique solution.
