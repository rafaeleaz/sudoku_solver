from helpers import *
import itertools


class Sudoku:

    def __init__(self, board=[["." for i in range(9)] for j in range(9)], marks=[[[str(n+1) for n in range(9)] for m in
                                                                                  range(9)] for k in range(9)]):
        """
        Create an instance of a Sudoku puzzle, with 2-dimensional list board detailing the puzzle answers and
        3-dimensional list marks detailing the puzzle's pencil marks. The int answers records the number of tiles
        answered in the puzzle, and the boolean solved indicates the state of the puzzle (solved or unsolved).

        @param board: list[list[str]]
        @param marks: list[list[list[str]]]
        @rtype: None
        """
        self.board = board
        self.marks = marks
        self.answers = 0
        self.solved = False
        for row in self.board:
            for entry in row:
                if entry != ".":
                    self.answers += 1
        if self.answers == 81:
            self.solved = True

    def __str__(self):
        """
        Give a string representation for the Sudoku puzzle.

        @rtype: str
        """
        my_string = ""
        for row in self.board:
            for entry in row:
                my_string += " " + entry + " "
            my_string += "\n"
        return my_string

    def remove_marks(self, answers, tiles):
        """
        Delete the answers in answers from self´s marks at the positions given by tiles. Return True if changes are made
        to self.marks, and False otherwise.

        @param answers: list[str]
        @param tiles: list[list[int]]
        @rtype: bool
        """
        changed = False
        for char in answers:
            for tile in tiles:
                if char in self.marks[tile[0]][tile[1]]:
                    changed = True
                    self.marks[tile[0]][tile[1]].remove(char)
        return changed

    def pencil_marks(self):
        """
        Populates the "pencil marks" i.e. all of the possible answers for each tile of a given sudoku puzzle, structured
        as a 3-dimensional array, where the first dimension represents the rows of the puzzle, the second corresponds
        to the columns, and the third corresponds to the possible answers of the tile given by the first two dimensions.

        @rtype: None
        """
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == ".":
                    continue
                self.marks[row][column] = []
                cousins = get_cousins(row, column)
                self.remove_marks([self.board[row][column]], cousins)

    def write_answer(self, answer, row, column):
        """
        Write the answer answer in self's board at position (row, column), and delete the pencil marks in self's
        marks which are no longer allowable. Return True.

        @param answer: str
        @param row: int
        @param column: int
        @rtype: bool
        """
        self.board[row][column] = answer
        self.marks[row][column] = []
        self.answers += 1
        cousins = get_cousins(row, column)
        self.remove_marks([answer], cousins)
        return True

    def fill_one_pm(self):
        """
        Write the only possible answer in each tile which only has one item in its pencil marks list. Return True if
        changes are made, and False otherwise.

        @rtype: bool
        """
        changed = False
        for row in range(9):
            for column in range(9):
                if len(self.marks[row][column]) == 1:
                    changed = self.write_answer(self.marks[row][column][0], row, column)
        return changed

    def only_tile(self, tiles):
        """
        Write each answer which has only one possibe position among tiles, in its corresponding tile. Return True if any
        answers are written, and False otherwise.

        @param tiles: list[list[int]]
        @rtype: bool
        """
        changed = False
        for digit in range(1, 10):
            answer = str(digit)
            counter = 0
            first_occurrence = []
            for tile in tiles:
                if answer in self.marks[tile[0]][tile[1]]:
                    if counter == 0:
                        first_occurrence = tile
                    counter += 1
            if counter == 1:
                self.write_answer(answer, first_occurrence[0], first_occurrence[1])

                changed = True
        return changed

    def fill_one_tile(self):
        """
        Write each answer which has only one possible place at each row, column, and square, in its correponding tile.
        Return True if any answers are written, and False otherwise.

        @rtype: bool
        """
        changed = False
        for row in range(9):
            tiles = [[row, i] for i in range(9)]
            if self.only_tile(tiles):
                return True
        for column in range(9):
            tiles = [[i, column] for i in range(9)]
            if self.only_tile(tiles):
                return True
        for square in range(9):
            tiles = tiles_from_square(square)
            if self.only_tile(tiles):
                return True
        return changed

    def find_matches(self, length, tiles):
        """
        Delete a sequence of length length of answers from all but length tiles from tiles, if these length tiles have
        as pencil marks ONLY the answers from our sequence.

        @param length: int
        @param tiles: list[list[int]]
        """
        changed = False
        candidates = [tile for tile in tiles if len(self.marks[tile[0]][tile[1]]) <= length and self.board[tile[0]][tile[1]] == "."]
        if len(candidates) < length:
            return False
        possible_matches = itertools.combinations(candidates, length)
        for match in possible_matches:
            answer_pool = []
            for tile in match:
                answer_pool += self.marks[tile[0]][tile[1]]
            answer_pool = set(answer_pool)
            if len(answer_pool) == length:
                leftover_tiles = [tile for tile in tiles if tile not in match]
                changed = self.remove_marks(answer_pool, leftover_tiles)
        return changed

    def eliminate_marks(self):
        """
        Delete all possible answers from marks, which cannot be correct answers in the puzzle without causing conflicts,
        as specified in the README file. Return True if any marks are deleted, and False otherwise.

        @rtype: bool
        """
        for length in [2, 3, 4]:
            for row in range(9):
                tiles = [[row, i] for i in range(9)]
                if self.find_matches(length, tiles):
                    return True
            for column in range(9):
                tiles = [[i, column] for i in range(9)]
                if self.find_matches(length, tiles):
                    return True
            for square in range(9):
                tiles = tiles_from_square(square)
                if self.find_matches(length, tiles):
                    return True
        return False

    def sudoku_solver(self):
        """
        Modifies the sudoku puzzle board in-place with the correct answers (assuming that they exist). Return True if
        the puzzle is solved, or False if it cannot be solved.

        @rtype: bool
        """
        self.pencil_marks()
        while not self.solved:
            if self.fill_one_pm():
                continue
            if self.fill_one_tile():
                continue
            if self.eliminate_marks():
                continue
            return True
        return False
