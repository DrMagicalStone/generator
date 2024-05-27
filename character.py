from random import randint

charsetCap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def generateRandomString(length: int):
    charset = charsetCap
    
    builder = ""
    for times in range(0, length):
        builder = builder + charset[randint(0, len(charset) - 1)]
    return builder