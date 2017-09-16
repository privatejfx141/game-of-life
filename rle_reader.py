from pprint import pprint
from patterns import draw_pattern

RLE_DEAD, RLE_ALIVE = 'b', 'o'
DEAD, ALIVE = 0, 1


def read_rle(file_handle):
    """(io.TextIOWrapper) -> dict of {str: int, str: int, str: str}"""
    length = height = None
    sequence = ''
    # Loop through each line in the file handle.
    for line in file_handle:
        # Get length and height of the pattern.
        if line[0:4] == 'x = ':
            contents = line.strip().split(', ')
            length = int(contents[0].split()[-1])
            height = int(contents[1].split()[-1])
        # Once length and height are read, read the RLE sequence.
        elif length and height:
            sequence += line.strip()
    # Return the processed data.
    return {'l': length, 'h': height, 'seq': sequence}


def read_sequence(sequence):
    """(str) -> list of list"""
    pattern = list()

    # Loop through each portion of the sequence.
    for row in sequence[:-1].split('$'):
        pattern.append(list())
        repeat = ''
    
        # Loop through each char.
        for char in row:
            # If char is letter ('o', 'b'), add cells.
            if char.isalpha():
                repeat = 1 if repeat == '' else int(repeat)
                if char == RLE_ALIVE:
                    pattern[-1] += [ALIVE] * repeat
                else:
                    pattern[-1] += [DEAD] * repeat
                repeat = ''
            # If char is a number, add onto repeat factor.
            else:
                repeat += char
    
    # Fix any uneven rows of the pattern.
    pattern_length = len(max(pattern, key=len))
    for r in range(len(pattern)-1, -1, -1):
        if len(pattern[r]) < pattern_length:
            pattern[r] += [DEAD] * (pattern_length-len(pattern[r]))

    # Return the read pattern.
    return pattern


if __name__ == '__main__':
    
    """
    # Garden of Eden 1 RLE sequence.
    eden1_seq = '33o$2obob3ob3ob2obobobobobobobobobo$'
    eden1_seq += 'obob3ob3ob4ob3obobobobobobob$5ob3ob3ob4ob14o'
    eden1_seq += '$obob2ob3ob3obob3obobobobobobob$4ob3ob3ob5ob2obobobobobobo$b'
    eden1_seq += '2ob3ob3ob3obobob13o$2ob2ob3ob3ob2ob4obobobobobobo$18ob14o!'
    # Garden of Eden 3 RLE sequence.
    eden3_seq = '2bob3o6b$2obob5obob$obob2obobo3b$b4obob3o2b$obob2ob3obob$'
    eden3_seq += 'b3ob2obobo2b$2bo3b3o2b2o$bob2obobob2ob$3ob4obobob$'
    eden3_seq += 'bob4o3bo2b$bobob2o2bo3b$b2obo2b2o2bo!'
    # Garden of Eden 6 RLE sequence.
    eden6_seq = 'bob3obo$2bobobo2bo$ob3o2b2o$bob5obo$o2bo2b4o$4o2bo2bo$ob5obo$'
    eden6_seq += 'b2o2b3obo$o2bobobo$2bob3obo!'

    # Read and draw a glider RLE sequence.
    print(draw_pattern(read_sequence('bob$2bo$3o!')))
    """

    """
    steamship_data = read_rle(open('steamship.rle', 'r'))
    steamship = read_sequence(steamship_data['seq'])
    print(steamship)
    print(steamship_data['l'], steamship_data['h'])
    print(draw_pattern(steamship))
    """

    pattern = read_sequence('2o7b2o2b2o2b2o2b2o2b2o2b2o2b2o5b$2o4bob3o2b2o2b2o2b2o2b2o2b2o2b2o3b2o$4b2obo29bobo$4b2o3b29o2b$4b2obo30bob$2o4bob3o2b2o2b2o2b2o2b2o2b2o2b2o2b2ob$2o7b2o2b2o2b2o2b2o2b2o2b2o2b2o!')
    print(draw_pattern(pattern))
