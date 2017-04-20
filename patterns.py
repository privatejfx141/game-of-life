def draw_pattern(pattern):
    """(list of list) -> str

    Return the string representation of pattern.
    """
    res = ''
    num_rows, num_cols = len(pattern), len(pattern[0])
    # Loop through each cell.
    for r in range(num_rows):
        for c in range(num_cols):
            res += 'o' if pattern[r][c] else '.'
            if c != num_cols- 1:
                res += ' '
        if r != num_rows - 1:
            res += '\n'
    # Return the string representation.
    return res


STILL_LIFE = {
    'block': [[1, 1], [1, 1]],
    'tub': [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ],
    'boat': [
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ],
    'beehive': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ],
    'eater': [
        [1, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1]
    ]
}

SPACESHIP = {
    'glider': [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    'lwss': [
        [0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0]
    ],
    'steamship': [
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
    ]
}

AGAR = {
    'zebra': [
        [1] * 10,
        [0] * 10,
        [1] * 10,
        [0] * 10,
        [1] * 10,
        [0] * 10
    ]
}

METHUSELAH = {
    'r-pentomino': [
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0]
    ],
    'acorn': [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1]
    ],
    'b-heptomino': [
        [1, 0, 1, 1],
        [1, 1, 1, 0],
        [0, 1, 0, 0]
    ],
    'pi-heptomino': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1]
    ]
}

COMMON = {
    'blinker': [[1, 1, 1]],
    'block': STILL_LIFE['block'],
    'glider': SPACESHIP['glider'],
    'r-pentomino': METHUSELAH['r-pentomino']
}


steamship = '''
...ooo...........ooo...
..o.................o..
...o..ooo.ooo.ooo..o...
.....o..o.o.o.o..o.....
.......oo.o.o.oo.......
.......o..o.o..o.......
..........o.o..........
.......o..o.o..o.......
........o.o.o.o........
........o.o.o.o........
.....oo.o.o.o.o.oo.....
.....oo.o.o.o.o.oo.....
..oo
'''


if __name__ == '__main__':
    print(draw_pattern(METHUSELAH['pi-heptomino']))
