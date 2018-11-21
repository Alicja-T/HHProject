from collections import defaultdict, deque


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

#assumption: sequence at this point is stripped of zeros and leading number that represents number of vertices
def Max_HH(sequence): #returns constructed graph
    size = len(sequence)
    index = list(range(size))
    edges = []
    vertices_d = []
    max = sequence[0]
    for i in range(max + 1):
        vertices_d.append(deque())
    i = 0
    vertices_left = size
    for v in sequence: #creating list of vertices by degrees
        vertices_d[v].append(i)
        i += 1
    while vertices_left > 0:
        updated_vertices = []
        while (len(vertices_d[max])==0):
            max -= 1
        start = vertices_d[max].popleft()
        next_max = max
        for i in range(next_max):
            while (len(vertices_d[next_max]) == 0):
                next_max -= 1
            end = vertices_d[next_max].popleft()
            edges.append([start, end])
            vertices_left -= 1
            if (next_max - 1 > 0):
                updated_vertices.append([next_max-1, end])
        print(vertices_left)
        i = 0
        for i in range(len(updated_vertices)):
            vertices_d[updated_vertices[i][0]].append(updated_vertices[i][1])
            i += 1
        vertices_left += len(updated_vertices) - 1
        print(vertices_left)
        print(edges)
    return edges

example1 = [7, 6, 5, 4, 3, 2, 1, 1, 1]
example2 = [2, 2, 2, 1, 1]
example3 = [3, 3, 2, 2, 1, 1]
petersen = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ]

print(Max_HH(petersen))
