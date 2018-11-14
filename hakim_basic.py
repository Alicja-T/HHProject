def check_parity(sequence):
    parity = sum(sequence) % 2
    return False if parity else True

def check_zeros(sequence):
    for item in sequence:
        if (item!=0):
             return False
    return True

def check_bound(sequence):
    max = len(sequence) - 1
    for item in sequence:
        if item > max:
            return False
    return True

def hhl(sequence):
    size = len(sequence)
    if (sequence[0] == 0):
        return True #zero graph

    #if (sequence[sequence[0]] == 0): ????
    #    return False
    if ( (sum(sequence) % 2 ) == 1 ):
        print("Sum of degrees is not even \n") # if sum is not even the sequence is not graphical
        return False
    weights = [0] * size
    reserve = [0] * size
    weights[0] = len(sequence) - 1
    while (sequence[weights[0]] < 1):
        weights[0]-= 1
    reserve[0] = weights[0] - 1 - sequence[0]
    index = 1
    while (index < size - 2):
        if (sequence[index] <= index + 1 or sequence[index + 1] == 0):
            return True
        weights[index] = weights[index-1]
        while (sequence[weights[index]] < index+1 and weights[index] > 0):
            weights[index] -= 1
        if (sequence[index] > weights[index]  + reserve[index-1]):
            return False
        reserve[index] = weights[index] + reserve[index - 1] - sequence[index]
        index += 1
        print("Reserve: " + str(reserve))
        print("Weights: " + str(weights))
    return True


example1 = [7, 6, 5, 4, 3, 2, 1, 1, 1]
example2 = [2, 2, 2, 1, 1, 1, 1]
example3 = [3, 3, 3, 3, 3]
print(sum(example1))
print(hhl(example1))
print(hhl(example2))
print(hhl(example3))
