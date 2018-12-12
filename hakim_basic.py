from collections import defaultdict, deque
from numpy.random import choice
import random

class Havel_Hakimi:

    def __init__(self, sequence):
        self.sequence = sequence
        self.size = len(sequence)

    def strip_zeros(self):
        i = self.size - 1
        while self.sequence[i] == 0 and i > 0:
            i -= 1
        self.sequence = self.sequence[:i+1]
        self.size = len(self.sequence)
        return self.sequence

    def is_graphic(self):
        self.sequence = self.strip_zeros()
        if ( (sum(self.sequence) % 2 ) == 1 ): # if sum is not even the sequence is not graphic
            return False
        if ( sum(self.sequence) == 0 ):
            return True
        weights = [0] * self.size
        reserve = [0] * self.size

        weights[0] = len(self.sequence) - 1
        while (self.sequence[weights[0]] < 1):
            weights[0]-= 1
        reserve[0] = weights[0] - self.sequence[0]
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

    def random_pivot(self, sequence, par=1):
        par_sum = 0
        for item in sequence:
            if item > 0:
                par_sum += item**par
        weights = []
        totals = []
        weights_sum = 0
        for item in sequence:
            if item > 0:
                new_weight = (item**par)/par_sum
            else:
                new_weight = 0
            weights.append( new_weight )
            weights_sum += new_weight
            totals.append(weights_sum)
        rn = random.random() * weights_sum
        i = 0
        while i < len(sequence):
            while sequence[i] == 0:
                i+=1
            if rn < totals[i]:
                break
            i+=1
        return i

#assumption: sequence at this point is stripped of zeros and leading number that represents number of vertices
    def Max_HH(self): #returns constructed graph
        if not self.is_graphic():
            return []
        if sum(self.sequence) == 0: #case of graph with zero edges
            return []
        edges = []
        vertices_d = []
        max_pivot = self.sequence[0]
        for i in range(max_pivot + 1): #n operations
            vertices_d.append(deque())
        i = 0
        vertices_left = self.size
        for v in self.sequence: #creating list of vertices by degrees
            vertices_d[v].append(i)
            i += 1
        while vertices_left > 0:
            updated_vertices = []
            while (len(vertices_d[max_pivot])==0):
                max_pivot -= 1
            start = vertices_d[max_pivot].popleft()
            next_max = max_pivot
            for i in range(next_max):
                while (len(vertices_d[next_max]) == 0):
                    next_max -= 1
                end = vertices_d[next_max].popleft()
                edges.append([start, end])
                vertices_left -= 1
                if (next_max - 1 > 0):
                    updated_vertices.append([next_max-1, end])
            i = len(updated_vertices) - 1
            for i in range(len(updated_vertices)):
                vertices_d[updated_vertices[i][0]].appendleft(updated_vertices[i][1])
                i -= 1
            vertices_left += len(updated_vertices) - 1
        return edges

    def Min_HH(self):
        if not self.is_graphic():
            return []
        if sum(self.sequence) == 0:
            return []
        edges = []
        vertices_d = []
        max_degree = self.sequence[0]
        next_max = max_degree
        min_pivot = 0
        for i in range(max_degree + 1):
            vertices_d.append(deque())
        i = 0
        vertices_left = self.size
        for v in self.sequence: #creating list of vertices by degrees
            vertices_d[v].append(i)
            i += 1
        while vertices_left > 0:
            updated_vertices = []
            min_pivot = 1
            while (len(vertices_d[min_pivot])==0): #getting a new min_pivot
                min_pivot += 1
            start = vertices_d[min_pivot].popleft() #O(1) because it's deque
            for i in range(min_pivot):
                next_max = max_degree
                while (len(vertices_d[next_max]) == 0):
                    next_max -= 1
                end = vertices_d[next_max].popleft()
                edges.append([start, end])
                vertices_left -= 1
                if (next_max - 1 > 0):
                    updated_vertices.append([next_max-1, end])
            i = 0
            for i in range(len(updated_vertices)):
                vertices_d[updated_vertices[i][0]].append(updated_vertices[i][1])
                i += 1
            vertices_left += len(updated_vertices) - 1
        return edges

    def Ur_HH(self):
        if not self.is_graphic():
            return []
        if sum(self.sequence) == 0:
            return []
        edges = []
        vertices_d = []
        sequence = self.sequence.copy()
        max_degree = self.sequence[0]
        next_max = max_degree
        min_pivot = 0
        for i in range(max_degree + 1):
            vertices_d.append( deque() )
        i = 0
        vertices_left = self.size
        for v in self.sequence: #creating list of vertices by degrees
            vertices_d[v].append(i)
            i += 1
        used_vertices = [False for i in range(self.size)]
        while vertices_left > 0:
            updated_vertices = []
            random_pivot = random.randint(0, self.size-1)
            while used_vertices[random_pivot] == True: #getting a new random_pivot
                random_pivot = random.randint(0, self.size-1)
            used_vertices[random_pivot] = True;
            index = sequence[random_pivot]
            for i in range( len(vertices_d[index]) ):
                if vertices_d[index][i] == random_pivot:
                    del vertices_d[index][i]
                    break
            start = random_pivot
            sequence[start] = 0
            for i in range(index):
                next_max = max_degree
                while (len(vertices_d[next_max]) == 0):
                    next_max -= 1
                end = vertices_d[next_max].popleft()
                edges.append([start, end])
                sequence[end] -= 1
                if (sequence[end] == 0):
                    used_vertices[end] = True
                vertices_left -= 1
                if (next_max - 1 > 0):
                    updated_vertices.append([next_max-1, end])
            i = 0
            for i in range(len(updated_vertices)):
                vertices_d[updated_vertices[i][0]].append(updated_vertices[i][1])
                i += 1
            vertices_left += len(updated_vertices) - 1
        return edges

    def Parr_HH(self, par=1):
        if not self.is_graphic():
            return []
        if sum(self.sequence) == 0:
            return []
        edges = []
        vertices_d = []
        sequence = self.sequence.copy()
        indexes = list( range(self.size) )
        max_degree = self.sequence[0]
        for i in range(max_degree + 1):
            vertices_d.append( deque() )
        i = 0
        vertices_left = self.size
        for v in self.sequence: #creating list of vertices by degrees
            vertices_d[v].append(i)
            i += 1
        next_max = max_degree
        while vertices_left > 0:
            updated_vertices = []
            rand_pivot = self.random_pivot(sequence, par)
            pivot_degree = sequence[rand_pivot]
            sequence[rand_pivot] = 0
            for i in range( len(vertices_d[pivot_degree]) ):
                if vertices_d[pivot_degree][i] == rand_pivot:
                    del vertices_d[pivot_degree][i]
                    break
            start = rand_pivot
            for i in range(pivot_degree):
                next_max = max_degree
                while (len(vertices_d[next_max]) == 0):
                    next_max -= 1
                end = vertices_d[next_max].popleft()
                edges.append([start, end])
                sequence[end] -= 1
                vertices_left -= 1
                if (next_max - 1 > 0):
                    updated_vertices.append([next_max-1, end])
            i = 0
            for i in range(len(updated_vertices)):
                vertices_d[updated_vertices[i][0]].append(updated_vertices[i][1])
                i += 1
            vertices_left += len(updated_vertices) - 1
        return edges


example1 = [7, 6, 5, 4, 3, 0, 0, 0, 0, 0]
example2 = [3, 3, 3, 3]
example3 = [3, 3, 2, 2, 1, 1]
petersen = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

#hh = Havel_Hakimi(example2)
#answer = hh.is_graphic()
#print(answer)
#edges = hh.Ur_HH()
#print(edges)
#edges = hh.Parr_HH(2)
#print(edges)
