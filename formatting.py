from patterns import *


def pattern_to_rle(pattern):
    """(list of list of int) -> str
    
    Convert and return the RLE string of the given pattern.
    """
    rle = ''
    count = 1
    for row in pattern:
        
        prev_cell = None
        for cell in row:
            
            if cell == prev_cell:
                count += 1
            
            else:
                if count != 1:
                    rle += str(count)
                rle += {0: 'b', 1: 'o'}[cell]
                count = 1
            
            prev_cell = cell
        
        if id(row) != id(pattern[-1]):
            rle += '$'
        else:
            rle += '!'
    
    return rle


if __name__ == '__main__':
    rle = pattern_to_rle(COMMON['glider'])
    for row in COMMON['glider']:
        print(row)
    print(rle)
