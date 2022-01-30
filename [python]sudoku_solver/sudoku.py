def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False


def used_in_row(arr, row, num):
    return num in arr[row]


def used_in_col(arr, col, num):
    return num in [arr[i][col] for i in range(9)]


def used_in_box(arr, row, col, num):
    row_box_th = row // 3
    col_box_th = col // 3
    for i in range(row_box_th*3, (row_box_th+1)*3):
        for j in range(col_box_th*3, (col_box_th+1)*3):
            if arr[i][j] == num:
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and \
           not used_in_col(arr, col, num) and \
           not used_in_box(arr, row, col, num)


def sudoku_solver(arr):
    l = [0, 0]
    if (not find_empty_location(arr, l)):
        return True
    
    row = l[0]
    col = l[1]
    for num in range(1, 10):
        if (check_location_is_safe(arr, row, col, num)):
            arr[row][col] = num
            if(sudoku_solver(arr)):
                return True
            arr[row][col] = 0
    return False


def sudoku_printer(arr):
    assert len(arr) == 9 and len(arr[0]) == 9
    for i in range(9):
        if i > 0 and i % 3 == 0:
            print('-' * 17)
        line = ''
        for j in range(9):
            if j > 0:
                if j % 3 == 0:
                    line += '|'
                else:
                    line += ' '
            line += str(arr[i][j])
        print(line)
    print('\n')