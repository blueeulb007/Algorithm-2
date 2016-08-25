__author__ = 'Zack Liu'


"""
    This Script implements the Union Find Data Structure with Union by Rank, and Path compression
"""

# Define the node struct
class node:
    def __init__(self, parent, rank, index ):
        node.parent = parent
        node.rank   = rank
        node.index  = index
class UnionFind:
    def __init__(self):
        #To hold the clusters
        self.clusters = []

    #create a new set(cluster) with a node
    def makeSet(self,node):
        #set the nodes parent to the node itself
        node.parent = node
        #set initial rank of node to 0
        node.rank = 0
        #set the index to its self
        node.index = node.index
        #add the node to cluster list
        self.clusters.append(node)

    #union the nodeA and nodeB clusters
    def union(self, nodeA, nodeB):

        self.link(self.findSet(nodeA), self.findSet(nodeB))

    #link the nodeA to nodeB or vice versa based upon the rank(number of nodes in the cluster) of the cluster
    def link(self, nodeA, nodeB):

        if nodeA.rank > nodeB.rank:
            nodeB.parent = nodeA
            #remove the nodeB from the cluster list, since it is merged with nodeA
            self.clusters.remove(nodeB)
        else:
            nodeA.parent = nodeB
            #remove the nodeA from the cluster list, since it is merged with nodeB
            self.clusters.remove(nodeA)
            #increade the rank of the cluster after merging the cluster
            if nodeA.rank == nodeB.rank:
                nodeB.rank = nodeB.rank + 1
    #find set will path compress(makes the nodes in cluster points to single leader/parent)  and returns the leader/parent of the cluster
    def findSet(self, node):

        if node != node.parent:
            node.parent = self.findSet(node.parent)
        return node.parent

    #get cluster size
    def clusterSize(self):
        return len(self.clusters)


