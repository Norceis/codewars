import random


def row_checker(row):
    full_set = set(range(1, 10))
    row_set = set(row)
    if 0 in row_set:
        row_set.remove(0)
    # print(full_set, row_set)
    available_numbers = full_set.difference(row_set)
    return available_numbers


def column_splitter(puzzle, column_number):
    return [puzzle[row][column_number] for row in range(len(puzzle))]


def hex_number_returner(row_number, column_number):
    hex_row_number = row_number // 3
    hex_column_number = column_number // 3
    if hex_row_number == 0:
        hex_number = hex_row_number + hex_column_number + 1
    elif hex_row_number == 1:
        hex_number = hex_row_number + hex_column_number + 3
    elif hex_row_number == 2:
        hex_number = hex_row_number + hex_column_number + 5

    return hex_number


def hex_checker(puzzle, hex_number):
    numbers_in_hex = []
    for row in range(len(puzzle)):
        for column in range(len(puzzle)):
            temporary_hex_number = hex_number_returner(row, column)
            if hex_number == temporary_hex_number:
                numbers_in_hex.append(puzzle[row][column])

    return numbers_in_hex


def forward_step(puzzle, backtrack, dictionary_of_changes):
    if not backtrack:
        for row_number in range(len(puzzle)):
            for column_number in range(len(puzzle)):
                if puzzle[row_number][column_number] == 0:
                    available_numbers_row = row_checker(puzzle[row_number])

                    splitted_column = column_splitter(puzzle, column_number)
                    available_numbers_column = row_checker(splitted_column)

                    hex_number = hex_number_returner(row_number, column_number)
                    numbers_in_hex = hex_checker(puzzle, hex_number)
                    available_numbers_hex = row_checker(numbers_in_hex)

                    available_numbers = list(
                        available_numbers_row.intersection(available_numbers_column, available_numbers_hex))
                    try:
                        chosen_number = available_numbers[-1]
                        puzzle[row_number][column_number] = chosen_number
                        available_numbers.remove(chosen_number)
                        dictionary_of_changes[(row_number, column_number)] = available_numbers
                        return puzzle, backtrack, dictionary_of_changes
                    except:
                        puzzle[row_number][column_number] = 0
                        backtrack = True
                        return puzzle, backtrack, dictionary_of_changes
                # else:
                #     return puzzle, backtrack, dictionary_of_changes
    else:
        return puzzle, backtrack, dictionary_of_changes

def backward_step(puzzle, backtrack, dictionary_of_changes):
    if backtrack:
        for row_number in range(len(puzzle)):
            for column_number in range(len(puzzle)):
                # if bool(list(dictionary_of_changes.keys())):
                if (row_number, column_number) == list(dictionary_of_changes.keys())[-1]:
                    if not bool(dictionary_of_changes[(row_number, column_number)]):
                        del dictionary_of_changes[(row_number, column_number)]
                        puzzle[row_number][column_number] = 0
                        if not bool(dictionary_of_changes):
                            backtrack = False
                        return puzzle, backtrack, dictionary_of_changes

                    else:
                        chosen_number = random.choice(list(dictionary_of_changes[(row_number, column_number)]))
                        puzzle[row_number][column_number] = chosen_number
                        updated_available_numbers = dictionary_of_changes[(row_number, column_number)].remove(
                            chosen_number)
                        if updated_available_numbers is None:
                            updated_available_numbers = []
                        dictionary_of_changes[(row_number, column_number)] = updated_available_numbers
                        backtrack = False
                        return puzzle, backtrack, dictionary_of_changes
                # else:
                #     return puzzle, backtrack, dictionary_of_changes
    else:
        return puzzle, backtrack, dictionary_of_changes

def zero_checker(puzzle):
    finished = True
    for row_number in range(len(puzzle)):
        for column_number in range(len(puzzle)):
            if puzzle[row_number][column_number] == 0:
                finished = False
    return finished

def sudoku(puzzle):
    dictionary_of_changes = dict()
    backtrack = False
    while True:
        puzzle, backtrack, dictionary_of_changes = forward_step(puzzle, backtrack, dictionary_of_changes)
        puzzle, backtrack, dictionary_of_changes = backward_step(puzzle, backtrack, dictionary_of_changes)
        finished = zero_checker(puzzle)
        if finished:
            return puzzle

# puzzlerino = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
#           [6, 0, 0, 1, 9, 5, 0, 0, 0],
#           [0, 9, 8, 0, 0, 0, 0, 6, 0],
#           [8, 0, 0, 0, 6, 0, 0, 0, 3],
#           [4, 0, 0, 8, 0, 3, 0, 0, 1],
#           [7, 0, 0, 0, 2, 0, 0, 0, 6],
#           [0, 6, 0, 0, 0, 0, 2, 8, 0],
#           [0, 0, 0, 4, 1, 9, 0, 0, 5],
#           [0, 0, 0, 0, 8, 0, 0, 7, 9]]

puzzlerino = [[0, 0, 0, 0, 0, 0, 6, 1, 0],
          [7, 0, 0, 4, 0, 0, 0, 0, 0],
          [2, 0, 0, 3, 0, 0, 0, 0, 0],
          [3, 0, 0, 0, 5, 0, 0, 0, 2],
          [0, 4, 9, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 6, 0, 0, 0, 0],
          [0, 1, 6, 0, 0, 0, 9, 0, 0],
          [0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 0, 0, 7, 0, 0, 0, 0, 0]]

solution = sudoku(puzzlerino)
[print(x) for x in solution]
