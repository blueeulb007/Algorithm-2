__author__ = 'Zack Liu'
import numpy as np

"""
    This script implements the Knapsack algorithm using DP.
    Implementation may vary depending on the problem size
"""

# #### Question 1
#f = open("knapsack1.txt")
f = open("knapsack_big.txt")
rawdata = f.readlines()
VList = []
WList = []
for i in range(len(rawdata)):
    tmp = rawdata[i]
    tmp = tmp.splitlines()
    tmp = tmp[0]
    tmp = tmp.split()
    if i == 0:
        W  = int(tmp[0])
        N  = int(tmp[1])
    else:
        VList.append(int(tmp[0]))
        WList.append(int(tmp[1]))

f.close()

# Naive Implementation is sufficent for Q1
# A = [ [0] * (W+1) for i in range(N + 1)] # N+1 * W+1 2-D Matrix
#
# for i in range(1, N+1): # for 1, 2,3,...,N
#     for x in range(W+1): # for 0, 1,2,3,....W
#         wi = WList[i-1]
#         vi = VList[i-1]
#         if x < wi:
#             A[i][x] = A[i-1][x]
#         else:
#             A[i][x] = max(A[i-1][x], A[i-1][x-wi] + vi)
#
# print(A[N][W])


# Optimized Implementation
A = [0] * (W+1)
A = np.array(A)
for i in range(N):
    print(i)
    vi = VList[i]
    wi = WList[i]

    idx = list(range(wi,W+1))
    idxnp = np.array(idx)
    A[idxnp] = np.maximum(A[idxnp - wi] + vi, A[idxnp])

print(A[W])