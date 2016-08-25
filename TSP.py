__author__ = 'Zack Liu'

"""
    Programming Assignment 5 - Travelling Salesman Problem

    This is the naive implementation of the DP algorithm. Takes around 30mins to run
"""
import numpy as np
from scipy.spatial.distance import pdist, squareform # used to calculate the Eculi distance
import itertools
import math



def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

filename = "tsp.txt"
#filename = "tspTest.txt"
f = open(filename)
rawdata = f.readlines()
nparrList = []

for i in range(len(rawdata)):
    tmp = rawdata[i]
    tmp = tmp.splitlines()
    tmp = tmp[0]
    tmp = tmp.split()
    if i == 0:
        n  = int(tmp[0])
    else:
        Xtmp = float(tmp[0])
        Ytmp = float(tmp[1])
        nparrList.append(np.array([[Xtmp, Ytmp]]))

f.close()

# Constrcut the euclidean distance matrix
nparr = np.concatenate(nparrList,axis =0 )
d = squareform(pdist(nparr, 'euclidean'))

# Create a distance dictionary for O(1) look up
ddict = {}
for i in range(n):
    for j in range(n):
        ddict[(i+1,j+1)] = d[i][j]

# Create a set S to index array mapping.
# E.g, when m = 2,
# {1,2} -> 1, {1,3} -> 2, {1,4} -> 3, ...., {1,n} -> n-1
s2idxdict = {}
p = list(range(1,n+1))
for m in range(2, n):
    c = itertools.combinations(p,m)
    idx = 1
    for i in c:
        tmpSet = tuple(i)
        if 1 in tmpSet:
            s2idxdict[tmpSet] = idx
            idx += 1

# add the base case
s2idxdict[(1,)] = 1
s2idxdict[tuple(range(1, n+1))] = 1

Aprev  = np.full((n-1,1), 100000)
Aprev[0][0] = 0 # i.e A[{1}, 1] = 0

# Proceed to the DP algorithm
# when m = 2, size of S = 2, namely S = {1,2}, {1,3}, ...., {1,25}
for m in range(2,n+1): # m = 2, 4, 5, 6, ..., n
    print(m)
    tmpNs = round(nCr(n-1, m-1))
    tmpNj = m - 1
    Acurr = np.zeros((tmpNs,tmpNj))
    slist = [key for key, value in s2idxdict.items() if len(key) == m]
    slist = sorted(slist)
    for i in range(tmpNs): # Iterate through each Set S of size m that contains 1
        s     = slist[i]
        for idxj in range(1,len(s)): # Iterate through each j in S that j != 1
            j = s[idxj]
            sprev = tuple(set(s) - {j}) # this the s - {j}
            sprev = tuple(sorted(sprev))
            if m > 2:
                sprevIter = sprev[1:]
            else:
                sprevIter = sprev
            distList = []
            sprevIdx = 0
            for k in sprevIter:
                AprevIdx = s2idxdict[sprev]
                distList.append(Aprev[AprevIdx-1][sprevIdx] + ddict[(k, j)] )
                sprevIdx += 1
            Acurr[i][idxj-1] = min(distList)
    Aprev = Acurr


# Final Step, find the minimum
distList = []
for i in range(n-1):
    j = i + 2
    distList.append(Acurr[0][i] + ddict[(j, 1)] )

print("The min distance rounded to the nearest interger is %d" % round(int(distList)))



