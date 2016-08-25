__author__ = 'Zack Liu'
"""
    The script implements 3 questions in Programming Assignment #1
"""


#### Question 1 & 2
f = open("jobs.txt")
rawdata = f.readlines()
Weights = []
Lengths  = []
diff     = []
ratio    = []
for i in range(len(rawdata)):
    dataiter = rawdata[i]
    dataiter = dataiter.splitlines()
    if i == 0:
        numJobs = int(dataiter[0])
    else:
        dataiter = dataiter[0]
        dataiter = dataiter.split()
        weightiter = int(dataiter[0])
        lengthiter = int(dataiter[1])

        Weights.append(weightiter)
        Lengths.append(lengthiter)

        diff.append(weightiter - lengthiter)
        ratio.append(weightiter/lengthiter)
f.close()

# construct the list of (difference, weight) to schedule the jobs
diffweightList = [(diff[j],Weights[j]) for j in range(numJobs)]
diffweightListSorted    = sorted(diffweightList, reverse = True)

# Construct the list of (ratio, weight) to schedule the jobs
ratioweightList = [(ratio[j], Weights[j]) for j in range(numJobs)]
ratioweightListSorted = sorted(ratioweightList, reverse = True)

SumWeightedCompTimeDiff = 0
CompTimeDiff    = 0

SumWeightedCompTimeRatio = 0
CompTimeRatio   = 0

for i in range(numJobs):
    (DIter, WIter) = diffweightListSorted[i]
    LIter = WIter - DIter
    CompTimeDiff += LIter
    SumWeightedCompTimeDiff += WIter * CompTimeDiff

    (RIter, WIter) = ratioweightListSorted[i]
    LIter = WIter / RIter
    CompTimeRatio += LIter
    SumWeightedCompTimeRatio += WIter * CompTimeRatio


# Print results for Q1 and Q2
print(SumWeightedCompTimeDiff)
print(SumWeightedCompTimeRatio)

############# Q3
f = open("edges.txt")
rawdata = f.readlines()
OrigGraph = {}

for i in range(len(rawdata)):
    tmp = rawdata[i]
    tmp = tmp.splitlines()
    tmp = tmp[0]
    tmp = tmp.split()
    if i == 0:
        nV  = int(tmp[0])
        nE  = int(tmp[1])
    else:
        if not OrigGraph.__contains__(int(tmp[0])):
            OrigGraph[int(tmp[0])] = []
        if not OrigGraph.__contains__(int(tmp[1])):
            OrigGraph[int(tmp[1])] = []

        OrigGraph[int(tmp[0])].append((int(tmp[1]), int(tmp[2])))
        OrigGraph[int(tmp[1])].append((int(tmp[0]), int(tmp[2])))

f.close()
print("Reading Graph Done")

#Naive Implementation
V = set(OrigGraph.keys())
X = {1}
Cost = 0

while X != V:
    vEdges = []
    for u in X:
        # We only select the edges u-v where u in X and v not in X
        vEdgesIter  = OrigGraph[u]
        vEdgesIter  = [(vx, d) for (vx, d) in vEdgesIter if vx not in X]

        vEdges.extend(vEdgesIter)

    sortedVEdges = sorted(vEdges, key = lambda x: x[1])

    e = sortedVEdges[0]
    X.add(e[0])
    Cost += e[1]

print(Cost)


