import re

DEAD = 0
ALIVE = 1
COMMENTS = {
    'C': "comment",
    'N': "name",
    'O': "author",
    'P': "tl-life32",
    'R': "tl-xlife",
    'r': "rules"
}


def read_rle_file(file_path: str) -> dict:
    """(str) -> dict of {str: value}

    Reads a run-length encoded file and returns a dictionary of results.
    """
    result = dict()
    file_handle = open(file_path, "r")
    for line in file_handle:
        line = line.strip()
        # if line is a comment
        if line[0] == '#':
            line = line[1:].strip()
            index = line.find(' ')
            letter, desc = line[:index], line[index+1:]
            if letter.upper() == 'C':
                key = COMMENTS['C']
                if key in result:
                    result[key] += '\r\n' + desc
                else:
                    result[key] = desc
            elif letter in COMMENTS:
                result[COMMENTS[letter]] = desc
            else:
                result[letter] = desc
        # if line is a header line
        elif line[0] in ('x', 'y'):
            result['header'] = line
        # if line is part of the sequence
        else:
            line = re.sub(r'\s+', '', line)
            if "pattern" in result:
                result["pattern"] += line
            else:
                result["pattern"] = line
    return result


def parse_sequence(sequence: str) -> [[int]]:
    """(str) -> list matrix of int

    Parses a Game of Life pattern sequence encoded in the RLE format.

    :param sequence: RLE sequence representing the pattern
    :return: a matrix of integers representing the pattern

    >>> _print_pattern(parse_sequence("bo$2bo$3o!"))
    . o
    . . o
    o o o
    >>> _print_pattern(parse_sequence("b2o$2ob$bo!"))
    . o o
    o o .
    . o
    >>> _print_pattern(parse_sequence("bo4b$obo3b$b2o3b$3b2ob$3bobo$4bo!"))
    . o . . . .
    o . o . . .
    . o o . . .
    . . . o o .
    . . . o . o
    . . . . o
    """
    sequence = re.sub(r'\s+', '', sequence)
    petri_dish = list()
    for line in sequence.split(sep="$"):
        cell_line = list()
        for match in re.findall(r'(\d*\w)', line):
            is_alive = match[-1] == 'o'
            repeat = int(match[:-1]) if match[:-1] else ALIVE
            cell_line += repeat * [ALIVE if is_alive else DEAD]
        petri_dish.append(cell_line)
    return petri_dish


def print_pattern_info(pattern_info: dict) -> None:
    keys = list(pattern_info.keys())
    keys.sort()
    for key in keys:
        print(key + ':')
        print(pattern_info[key] + '\n')


def _print_pattern(pattern_mtx: [[int]]) -> None:
    for cell_list in pattern_mtx:
        str_list = ['o' if cell == ALIVE else '.' for cell in cell_list]
        print(" ".join(str_list))


def encode_rle(pattern_mtx: [[int]]) -> str:
    NotImplemented


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    test_file_path = "pattern\\spaceship\\glider.rle"
    test_pattern_info = read_rle_file(test_file_path)
    print_pattern_info(test_pattern_info)
    parsed = parse_sequence(test_pattern_info['pattern'])
    print(parsed)
