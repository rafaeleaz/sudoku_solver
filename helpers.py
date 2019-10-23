def get_square(row, column):
    """
    Calculate the number of the large square to whic a tile with coordinates (row, column) belongs.

    @param row: int
    @param column: int
    @rtype: int
    """
    return (row // 3) * 3 + (column // 3)


def tiles_from_square(square):
    """
    List the coordinates of all the tiles contained in a large square, square, of a Sudoku board.

    @param square: int
    @rtype: list[list[int]]
    """
    big_row = square // 3
    big_column = square % 3
    tiles = []
    for i in range(3):
        for j in range(3):
            next_tile = [3 * big_row + i, 3 * big_column + j]
            tiles.append(next_tile)
    return tiles


def get_cousins(row, column):
    """
    Enumerate the coordinates of all tiles (i.e. cousins) which share a row, a column, or a large square with the tile
    whose coordinates are (row, column).

    @param row: int
    @param column: int
    @rtype: list[list[int]]
    """
    square_cousins = tiles_from_square(get_square(row, column))
    row_cousins = [[row, i] for i in range(9)]
    column_cousins = [[i, column] for i in range(9)]
    cousins = square_cousins + row_cousins + column_cousins
    return cousins
