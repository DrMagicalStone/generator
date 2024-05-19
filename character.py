from random import randint

charsetCap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü', 'ß', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '^', ' ', ' ', '  ', '     ']
charsetLow = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'y', 'z', 'ä', 'ö', 'ü', 'ß', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '^', ' ', ' ', '  ', '     ']

def generateRandomString(length: int):
    if (randint(0, 1) == 0):
        charset = charsetCap
    else:
        charset = charsetLow
    
    builder = ""
    for times in range(0, length):
        builder = builder + charset[randint(0, len(charset) - 1)]
    return builder