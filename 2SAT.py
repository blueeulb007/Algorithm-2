__author__ = 'Zack Liu'

"""
    This script implements the 2-SAT problem.
    Use the Finding Strong Connected Component algorithm on implication graph

    Need to modify the SCC.py that was implemented in part 1 of the course
"""
import SCC

for i in range(1,7):
    filename = "2sat" + str(i) +".txt"

    (OrigGraph, ReverseGraph) = SCC.LoadGraphs(filename)

    print("Done with Constructing Implication Graph and Its Reverse Graph")

    # First DFS loop to get the finish time
    finish_time_dic = SCC.DFSIterativeFindFinishingTime(ReverseGraph)
    print("Done with First DFS Loop to Calculate the Finishing Time")

    # Sort the finish time
    keyValPairSorted = sorted([(value,key) for (key, value) in finish_time_dic.items() ], reverse = True)
    KeyList = [k for (foo,k) in keyValPairSorted]
    print("Done with Sorting the Finishing time and Value")

    # Second DFS loop to get the Strong Connected componnets
    N = len(KeyList)
    LeaderDic = {}
    visited = set()
    OrigKey = list(OrigGraph.keys())

    SatisfyFlag = 1 # Iterate through all the strong connected components. As long as we find a vertex v and its negated value -v are in the same SCC, set this to 0, and return
    for v in KeyList:
        LeaderDic[v] = 0
        if OrigGraph.__contains__(v):
            if not v in visited:
               SatisfyFlag =  SCC.DFSIterative(OrigGraph,v,visited, LeaderDic)

        if SatisfyFlag == 0:
            break

    print("Done with Second DFS Loop")
    print("file - %s results: %d" %(filename,SatisfyFlag))


