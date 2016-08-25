__author__ = 'zhihao_liu'

"""
    This script runs the Kosaraju's two-pass algorithms
"""

def SCCAlgo(filename):

    (OrigGraph, ReverseGraph) = LoadGraphs(filename)

    ## DFS-loop subroutine on the Reverse Graph to find the f-values
    t = 0 # Initilize the global variable
    Explored = []
    ReverseKey = list(ReverseGraph.keys())
    NkeyReverse = len(ReverseKey)
    Leader = [0] * NkeyReverse
    fvalue = [0] * NkeyReverse

    for i in range(NkeyReverse):
        keyIter = ReverseKey[i]
        if not keyIter in Explored:
            s = keyIter
            t = DFS(ReverseGraph, i,ReverseKey,Explored,Leader,s,t,fvalue )

    print("fvalues in Reversed Graph:")
    print(ReverseKey)
    print(fvalue)


    # Second DFS-LOOP subroutine on G, processing vertices in decreasing order of f(v)
    t = 0
    Explored = []
    OrigKey = list(OrigGraph.keys())
    Nkey = len(OrigKey)
    fvalueCopy = fvalue[:]
    fvalueCopy1 = fvalue[:]
    Leader = [0] * Nkey
    fvalue = [0] * Nkey

    for i in range(NkeyReverse):
        maxIter = max(fvalueCopy)
        fvalueCopy.remove(maxIter)
        keyIter = ReverseKey[fvalueCopy1.index(maxIter)]

        if OrigGraph.__contains__(keyIter):
            idx = OrigKey.index(keyIter)
            if not keyIter in Explored:
                s = keyIter
                t = DFS(OrigGraph,idx,OrigKey, Explored, Leader,s,t,fvalue)

    print("The second loop")
    print(OrigKey)
    print(Leader)

    # Number of first five
    uniqueLeaderL = list(set(Leader))
    NumCount = [Leader.count(val) for val in uniqueLeaderL]
    NumCount.sort(reverse=True )
    if len(NumCount) <5:
        NumCount.extend([0] * (5 - len(NumCount)))

    print("Final Results")
    print(NumCount)

# thread = threading.Thread(target=go)
# thread.start()

def LoadGraphs(filename):
# First Construct the adjacent list of the Graph from the txt file
# At the same time; Construct the reverse Graph with all the edges reversed
    f = open(filename)
    OrigGraph = {}
    ReverseGraph = {}
    for line in f:
        tmp = line.splitlines()
        tmp = tmp[0]
        tmp = tmp.split(" ")

        if len(tmp) !=1:
            keytmp = int(tmp[0])
            valtmp = int(tmp[1])

            #Construct the implication graph
            # That is, keytmp valtmp => -keytmp valtmp and -valtmp keytmp in orig graph
            # Orig Graph
            if not OrigGraph.__contains__(-keytmp):
                OrigGraph[-keytmp] = set()
            OrigGraph[-keytmp].add(valtmp)

            if not OrigGraph.__contains__(-valtmp):
                OrigGraph[-valtmp] = set()
            OrigGraph[-valtmp].add(keytmp)

            # Reverse Graph
            if not ReverseGraph.__contains__(valtmp):
                ReverseGraph[valtmp] = set()
            ReverseGraph[valtmp].add(-keytmp)

            if not ReverseGraph.__contains__(keytmp):
                ReverseGraph[keytmp] = set()
            ReverseGraph[keytmp].add(-valtmp)

    f.close()

    # It is possible that in the Orig Graph that there are some "sinking vertices" , i.e., not outward edges. Initilize such node with empty []
    # This also applies to the Reverse Graph
    OrigGKeySet = set(list(OrigGraph.keys()))
    ReverseGKeySet = set(list(ReverseGraph.keys()))

    OrigGraphSinkV = ReverseGKeySet - OrigGKeySet
    ReverseGraphSinkV = OrigGKeySet - ReverseGKeySet

    for SinkV in OrigGraphSinkV:
        OrigGraph[SinkV] = set()
    for SinkV in ReverseGraphSinkV:
        ReverseGraph[SinkV] = set()

    return (OrigGraph, ReverseGraph)


def DFS(G, i, keysList, Explored, Leader, s, t, fvalue):
# G is the graph in adjacecy list
# i is the source vertex denoted by the i-th key in keyList of G(which is a dictionary), aka, keysList[i] = s

    Explored.append(keysList[i])

    # Leader only get value from the first DFS call; all successive DFS recursive calls do not update
    Leader[i] = s

    for j in G[keysList[i]]:
        if j in keysList: # not "Sinking Nodes"
            idx = keysList.index(j)
            if not j in Explored:
               t = DFS(G,idx,keysList, Explored,Leader,s,t, fvalue)

    t += 1
    fvalue[i] = t
    return t


def DFSIterative(Graph, s, visited, Leader):
    stack = []
    stack.append(s)
    visitedTmp = set()
    visitedTmp.add(s)
    while(len(stack)>0):
        v = stack.pop()
        if not v in visited:
            Leader[s] += 1
            visited.add(v)
            stack.extend(set(Graph[v]) - visited )

            visitedTmp.add(v)
            if -v in visitedTmp:
                return 0

    return 1


def DFSIterativeFindFinishingTime(ReversedGraph):
    visited = set()
    t = 1
    finish_time_dic = {}
    RevKeys = list(ReversedGraph.keys())
    for i in range(len(RevKeys)):

        s = RevKeys[i]

        stack = []
        stack.append(s)

        while(len(stack)>0):

            v = stack.pop()

            if not v in visited:
                visited.add(v)

                # The key is here - if some node v is not visited before, need to push it back to the stack for backtracking purpose
                stack.append(v)

                stack.extend(set(ReversedGraph[v]) - visited )
            else:
                if not v in finish_time_dic:
                    finish_time_dic[v] = t
                    t += 1

    return finish_time_dic
