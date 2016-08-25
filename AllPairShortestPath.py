__author__ = 'Zack Liu'
import numpy as np

"""
    This Script implements the all pair shortest path algorithms:
        - The Floyd-Warshall
        - Johnson's Algorithm
        - g1.txt, g2.txt and g3.txt are smaller graphs, while large.txt is a very big graph
"""

## Read the graph + initialize array A

def FloydWarshall(filename):
    f = open(filename)
    rawdata = f.readlines()
    Graph = {}

    for i in range(len(rawdata)):
        tmp = rawdata[i]
        tmp = tmp.splitlines()
        tmp = tmp[0]
        tmp = tmp.split()
        if i == 0:
            nV  = int(tmp[0])
            nE  = int(tmp[1])

            A = np.full( (nV, nV), 10000000)

        else:
            if not Graph.__contains__(int(tmp[0])):
                Graph[int(tmp[0])] = []

            Graph[int(tmp[0])].append( (int(tmp[1]), int(tmp[2])))

            A[int(tmp[0]) - 1][int(tmp[1]) -1] = int(tmp[2])



    f.close()
    np.fill_diagonal(A, 0)


    # Loops of Floyd-Warshall ALgorithm
    for k in range(nV):
        print(k)
        for i in range(nV):
            for j in range(nV):
                if A[i,k] + A[k,j] < A[i,j]:
                    A[i,j] = A[i,k] + A[k,j]

    # Check for negative cost cycle
    if min(A.diagonal()) < 0 : # There is negative cost cycle
        print("There is negative cost cycle in graph %s" % filename)
        return "NULL"
    else:
        return A.min()



