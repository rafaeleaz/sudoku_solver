def get_square(row, column):
    return (row // 3) * 3 + (column // 3)

def tiles_from_square(square):
    big_row = square // 3
    big_column = square % 3
    tiles = []
    for i in range(3):
        for j in range(3):
            next_tile = [3 * big_row + i, 3 * big_column + j]
            tiles.append(next_tile)
    return tiles


def pencil_marks(board):
    """
    Creates the "pencil marks" i.e. all of the possible answers for each tile of a given sudoku puzzle.

    @param list(list(str)) board: a Sudoku puzzle, formatted as a list of nine "rows", each of which has nine strings
    representing the digit of a particular tile if that tile has been answered, or "." otherwise.
    @rtype: list(list(list(str)))
    """
    marks = [[[]] * 9] * 9
    for row in range(9):
        for column in range(9):
            if board[row][column] != ".":
                continue
            pencil = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            square = tiles_from_square(get_square(row, column))
            for i in range(9):
                if board[row][i] in pencil:
                    pencil.remove(board[row, i])
                if board[i][column] in pencil:
                    pencil.remove(board[i][column])
                if board[square[i][0]][square[i][1]] in pencil:
                    pencil.remove(board[square[i][0]][square[i][1]])
            marks[row][column] = pencil
    return marks

def write_answer(answer, row, column, board, marks):
    board[row][column] = answer
    marks[row][column] = []
    square = tiles_from_square(get_square(row, column))
    for i in range(9):
        if answer in marks[row][i]:
            marks.remove(answer)
        if answer in marks[row][i]:
            marks.remove(answer)
        if answer in marks[square[i][0]][square[i][0]]:
            marks.remove(answer)
        return None

def fill_one_pm(board, marks):
    for row in range(9):
        for column in range(9):
            if len(marks[row][column]) == 1:
                write_answer(marks[row][column][0], row, column, board, marks)
    return None


def fill_one_tile(board, marks):
    for digit in range(1, 10):
        answer = str(digit)
        for row in range(9):
            counter = 0
            first_occurrence = -1
            for column in range(9):
                if board[row][column] == answer:
                    break
                if answer in marks[row][column]:
                    if counter >= 1:
                        break
                    counter += 1
                    first_occurrence = column
            if counter == 1:
                write_answer(answer, row, first_occurrence, board, marks)
        for column in range(9):
            counter = 0
            first_occurrence = -1
            for row in range(9):
                if board[row][column] == answer:
                    break
                if answer in marks[row][column]:
                    if counter >= 1:
                        break
                    counter += 1
                    first_occurrence = row
            if counter == 1:
                write_answer(answer, first_occurrence, column, board, marks)
        for square in range(9):
            counter = 0
            first_occurrence = []
            tiles = tiles_from_square(square)
            for tile in tiles:
                if board[tile[0]][tile[1]] == answer:
                    break
                if answer in marks[tile[0]][tile[1]]:
                    if counter >= 1:
                        break
                    counter += 1
                    first_occurrence = tile
            if counter == 1:
                write_answer(answer, first_occurrence[0], first_occurrence[1], board, marks)
    return None


def sudoku_solver(board):
    """
    Modifies the sudoku puzzle board in-place with the correct answers (assuming that they exist)

    @param list(list(str)) board: a Sudoku puzzle, formatted as a list of nine "rows", each of which has nine strings
    representing the digit of a particular tile if that tile has been answered, or "." otherwise.
    @rtype: None
    """
