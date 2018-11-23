from collections import defaultdict, deque

class Havel_Hakimi:

    def __init__(self, sequence):
        self.sequence = sequence
        self.size = len(sequence)

    def strip_zeros(self):
        i = self.size - 1
        while (self.sequence[i] == 0):
            i -= 1
        self.sequence = self.sequence[:i+1]
        return self.sequence

    def is_graphic(self):
        if ( (sum(self.sequence) % 2 ) == 1 ): # if sum is not even the sequence is not graphic
            return False
        weights = [0] * self.size
        reserve = [0] * self.size
        weights[0] = len(selfself.sequence) - 1
        while (self.sequence[weights[0]] < 1):
            weights[0]-= 1
        reserve[0] = weights[0] - 1 - self.sequence[0]
        index = 1
        while (index < self.size - 2):
            if (self.sequence[index] <= index + 1 or self.sequence[index + 1] == 0):
                return True
            weights[index] = weights[index-1]
            while (self.sequence[weights[index]] < index+1 and weights[index] > 0):
                weights[index] -= 1
            if (self.sequence[index] > weights[index]  + reserve[index-1]):
                return False
            reserve[index] = weights[index] + reserve[index - 1] - self.sequence[index]
            index += 1
        return True

#assumption: sequence at this point is stripped of zeros and leading number that represents number of vertices
    def Max_HH(self): #returns constructed graph
        index = list(range(self.size))
        edges = []
        vertices_d = []
        max = self.sequence[0]
        for i in range(max + 1):
            vertices_d.append(deque())
        i = 0
        vertices_left = self.size
        for v in self.sequence: #creating list of vertices by degrees
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


example1 = [7, 6, 5, 4, 3, 0, 0, 0, 0, 0]
example2 = [2, 2, 2, 1, 1]
example3 = [3, 3, 2, 2, 1, 1]
petersen = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3 ]
