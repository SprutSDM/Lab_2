import time


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    #print(digits)
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    for i in range(9):
        print(' '.join(values[i][0:3]) + ' | ' + ' '.join(values[i][3:6]) + 
              ' | ' + ' '.join(values[i][6:9]))
        if i == 2 or i == 5:
            print('------+-------+------')


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i * n:(i + 1) * n] for i in range(n)]


def get_row(grid, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [elem[pos[1]] for elem in grid]


def get_block(grid, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    #print(grid)
    i, j = pos[0] // 3 * 3, pos[1] // 3 * 3
    #print(i, j)
    ans = grid[i][j:j + 3]
    ans += grid[i + 1][j:j + 3]
    ans += grid[i + 2][j:j + 3]
    return ans


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return (i, j)
    return (-1, -1) # Если все позиции заняты


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции 
    
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    s = set([str(i) for i in range(1, 10)])
    r = get_row(grid, pos)
    c = get_col(grid, pos)
    b = get_block(grid, pos)
    for elem in r:
        if elem in s:
            s.remove(elem)
    for elem in c:
        if elem in s:
            s.remove(elem)
    for elem in b:
        if elem in s:
            s.remove(elem)
    return list(s)


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    position = find_empty_positions(grid)
    if position == (-1, -1):
        solution = []
        for elem in grid:
            solution.append([elements for elements in elem])
        return solution
    values = find_possible_values(grid, position)
    #print(values)
    for elem in values:
        grid[position[0]][position[1]] = elem
        solution = solve(grid)
        grid[position[0]][position[1]] = '.'
        if solution != None:
            return solution
    return None

def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    row = [set([str(i) for i in range(1, 10)]) for i in range(9)]
    col = [set([str(i) for i in range(1, 10)]) for i in range(9)]
    block = [set([str(i) for i in range(1, 10)]) for i in range(9)]
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            elem = solution[i][j]
            if elem not in row[i]:
                print('row')
                return False
            row[i].remove(elem)
            
            if elem not in col[j]:
                print('col')
                return False
            col[j].remove(elem)
            
            if elem not in block[i // 3 * 3 + j // 3]:
                print('block')
                return False
            block[i // 3 * 3 + j // 3].remove(elem)
    return True


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        print(fname + ':')
        display(grid)
        #print(grid)
        start = time.time()
        solution = solve(grid)
        end = time.time()
        print(end-start)
        print()
        print('Solution:')
        display(solution)
        print()
        print()