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
    adj_matrix = [0]*size
    for i in range(size):
        adj_matrix[i] = [0]*size
    working_seq = sequence
    inv_list = list(zip(sequence, index))
    vertices_d = defaultdict(list)
    for k, v in inv_list:
        vertices_d[k].append(v)
    max = sequence[0]
    next_max = sequence[1]
    while len(vertices_d) > 0:
        max_nodes = deque(vertices_d.get(max))
        nextmax_nodes = deque(vertices_d.get(next_max))
        first_node = max_nodes[0]
        print(max_nodes)
        print(nextmax_nodes)
        if (max==next_max):
            second_node = max_nodes[1]
        else:
            second_node = nextmax_nodes[0]
        if (adj_matrix[first_node][second_node] == 0):
            adj_matrix[first_node][second_node] = 1
            adj_matrix[second_node][first_node] = 1
            edges.append([first_node, second_node])
        else:
            i = 1 if max==next_max else 0
            while (adj_matrix[first_node][second_node] == 1 and i < len(nextmax_nodes) - 1):
                i += 1
                second_node = nextmax_nodes[i]
            adj_matrix[first_node][second_node] = 1
            adj_matrix[second_node][first_node] = 1
            edges.append([first_node, second_node])
        if (max==next_max):
            max_nodes.popleft()
            max_nodes.popleft()
            vertices_d.update({max : max_nodes})
            if (max - 1 > 0):
                vertices_d[max-1].append(first_node)
                vertices_d[max-1].append(second_node)
            print(vertices_d)
        else:
            max_nodes.popleft()
            next_nodes.popleft()
            vertices_d[max] = max_nodes
            vertices_d[next_max] = nextmax_nodes
            vertices_d[max-1].append(first_node)
            if (next_max - 1 > 0):
                vertices_d[next_max-1].append(second_node)
        working_seq[first_node] -= 1
        working_seq[second_node] -= 1
        print(vertices_d.get(max))
        while (vertices_d.get(max) == deque([])):
            max -= 1
            next_max -= 1
        print(max)
        print(edges)
        for i in range(size):
            print(adj_matrix[i])
    return edges

example1 = [7, 6, 5, 4, 3, 2, 1, 1, 1]
example2 = [2, 2, 2, 1, 1]
example3 = [3, 3, 2, 2, 1, 1]
petersen = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ]

print(Max_HH(petersen))
