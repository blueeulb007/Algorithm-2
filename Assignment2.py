__author__ = 'Zack Liu'
"""
    The script implementes the max-space k-clustering algorithm in assignment 2
"""
from Assignment2Helper import UnionFind,node
import numpy as np

# #### Question 1
f = open("clustering1.txt")
#f = open("text")
rawdata = f.readlines()
OrigGraph = {}
EdgeList = []
for i in range(len(rawdata)):
    tmp = rawdata[i]
    tmp = tmp.splitlines()
    tmp = tmp[0]
    tmp = tmp.split()
    if i == 0:
        nV  = int(tmp[0])
    else:
        # Create the EdgeList with the following element (v1,v2,cost)
        EdgeList.append(( int(tmp[0]), int(tmp[1]), int(tmp[2])))

f.close()
print("Reading Graph Done")

# Sorted the EdgeList according to the cost in an increasing order
SortedEdgeList = sorted(EdgeList, key = lambda x:x[2])

# Create a dictionary with (V1,V2) -> cost
keys = [(l[0],l[1]) for l in SortedEdgeList ]
values =[ l[2] for l in SortedEdgeList]
VtoCostdict = dict(zip(keys,values))

# Delete the Cost elements in SortedEdgeList
SortedEdgeList = keys

## Initialize the Union Find Data Structure
U = UnionFind()
nodeList = []
for i in range(nV):
    nodeIter = node(None,0, i + 1)
    nodeList.append(nodeIter)
    U.makeSet(nodeIter) # Initially every Vertex is a seperate node

# Run the greedy algorithm - Similar to the Kruskal's MST algorithm implemented using union-find data structure
k = 4
for i in range(len(SortedEdgeList)):
    Vpair = SortedEdgeList[i]
    V1 = Vpair[0]
    V2 = Vpair[1]
    node1 = nodeList[V1 - 1]
    node2 = nodeList[V2 - 1]

    if U.findSet(node1) != U.findSet(node2):# Not in the same Cluster yet
        U.union(node1, node2)

    if U.clusterSize() == k:
        break

# Need to find the maximum of k cluster spacing
clusterIter = U.clusters
curClusterIdx = set()
for i in range(U.clusterSize()):
    curClusterIdx.add(tuple([n.index for n in nodeList if n.parent == clusterIter[i]]))

curClusterIdx = list(curClusterIdx)
# At Last there are K clusters, we need to compare every two clusters
clusterIdx = [(i,j) for i in range(k) for j in range(k) if i < j]
maxClusterSpacing = 10000000 # Initialize to a larger number
for i in range(len(clusterIdx)):
    idxIter = clusterIdx[i]
    keys = [(a,b) if a < b else (b,a) for a in curClusterIdx[idxIter[0]] for b in curClusterIdx[idxIter[1]] ]
    SpacingIter = [VtoCostdict[x] for x in keys if VtoCostdict.__contains__(x)]
    if len(SpacingIter) == 0:
        continue
    clusterSpacingIter = min(SpacingIter)

    if clusterSpacingIter < maxClusterSpacing:
        maxClusterSpacing = clusterSpacingIter

print("The Max %d - cluster spacing is %d" % (k, maxClusterSpacing))

##### Q2
f = open("clustering_big.txt")
rawdata = f.readlines()
f.close()

binaryRepreList = [2 ** i for i in range(24)]
indx2binDict = {}
binSet = set()
idxcount = 1
for i in range(len(rawdata)):
    tmp = rawdata[i]
    tmp = tmp.splitlines()
    tmp = tmp[0]
    tmp = tmp.split()
    if i == 0:
        nV  = int(tmp[0])
        nbit = int(tmp[1])
    else:
        tmpBinary = [int(l) for l in tmp]
        tmpval  = np.dot(np.array(binaryRepreList), np.array(tmpBinary))
        if not tmpval in binSet:
            binSet.add(tmpval)
            indx2binDict[tmpval] = idxcount
            idxcount += 1

# Number for different node
N = len(indx2binDict)
ValList = list(indx2binDict.keys())
# distance 1 - list, i.e, binary representation is[0000000....1, 0000...10, ....., 10000...00]
dist1List = binaryRepreList

# distance 2 - list, i.e, binary representation is [000000....11,...., 11000000000000]
dist2List = [ l1 + l2 for l1 in dist1List for l2 in dist1List if l1 < l2]

# Similar to Q1 EdgeList
EdgeList = []

# Iterate Through all idxcount
for i in range(N):
    print(i)
    ValTMP = ValList[i]

    # distance 1
    dist1ResultList = [ValTMP ^ l for l in dist1List]
    for j in range(len(dist1ResultList)):
        if dist1ResultList[j] in binSet:
            toAppend = (indx2binDict[ValTMP],indx2binDict[dist1ResultList[j]], 1 ) if indx2binDict[ValTMP] < indx2binDict[dist1ResultList[j]] else \
                (indx2binDict[dist1ResultList[j]],indx2binDict[ValTMP], 1 )
            EdgeList.append(toAppend)

    # distance 2
    dist2ResultList = [ValTMP ^ l for l in dist2List]
    for j in range(len(dist2ResultList)):
        if dist2ResultList[j] in binSet:
            toAppend = (indx2binDict[ValTMP],indx2binDict[dist2ResultList[j]], 2) if indx2binDict[ValTMP] < indx2binDict[dist2ResultList[j]] else \
                (indx2binDict[dist2ResultList[j]],indx2binDict[ValTMP], 2)
            EdgeList.append(toAppend)

#
SortedEdgeList = sorted(EdgeList, key = lambda x:x[2])

l1List = [l[0] for l in SortedEdgeList]
l2List = [l[1] for l in SortedEdgeList]
print(l1List)
print(l2List)
SortedEdgeList = list(zip(l1List, l2List))
l1List.extend(l2List)
Vuse =list(set( l1List ))
nVused = len(Vuse)

# Create a mapping from Orginal Node Index to 0 - Vused-1
mapping = dict(zip(Vuse, list(range(nVused))))


# Run the Q1 algorithm but with different setting. When we finished all the edges, how many clusters there
## Initialize the Union Find Data Structure
U = UnionFind()
nodeList = []
for i in range(nVused):
    nodeIter = node(None,0, i)
    nodeList.append(nodeIter)
    U.makeSet(nodeIter) # Initially every Vertex is a seperate node

print("Start Running Greedy Algorithm")
# Run the greedy algorithm - Similar to the Kruskal's MST algorithm implemented using union-find data structure
for i in range(len(SortedEdgeList)):
    print( "%d / %d" % (i+1, len(SortedEdgeList) + 1))
    Vpair = SortedEdgeList[i]
    V1 = Vpair[0]
    V2 = Vpair[1]
    node1 = nodeList[mapping[V1]]
    node2 = nodeList[mapping[V2]]

    if U.findSet(node1) != U.findSet(node2):# Not in the same Cluster yet
        U.union(node1, node2)


# How many clusters?
print(N - nVused + U.clusterSize())
