from copy import deepcopy


def create_glider():
    glider = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ]
    return deepcopy(glider)


def create_block():
    block = [
        [1, 1],
        [1, 1]
    ]
    return deepcopy(block)


def create_blinker():
    blinker = [
        [1, 1, 1]
    ]
    return deepcopy(blinker)


def create_r_pentomino():
    pentomino = [
        [0, 1, 1],
        [1, 1, 0],
        [0, 1, 0]
    ]
    return deepcopy(pentomino)
