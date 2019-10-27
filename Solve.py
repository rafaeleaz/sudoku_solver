from Sudoku import Sudoku
import csv

csv_file = open('puzzles.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
puzzles = []
current_puzzle = []
line_counter = 0
for row in csv_reader:
    current_puzzle.append(row)
    if line_counter % 9 == 8:
        next_sudoku = Sudoku(current_puzzle)
        puzzles.append(next_sudoku)
        current_puzzle = []
    line_counter += 1

for puzzle in puzzles:
    puzzle.sudoku_solver()
    print(puzzle)
