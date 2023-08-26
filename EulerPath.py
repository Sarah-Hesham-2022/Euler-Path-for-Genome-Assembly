from typing import Sequence
import networkx, matplotlib.pyplot as plot 

def kmers(seq,k):
    return [seq[i:i+k] for i in range(len(seq)-k+1)]

def DeBruijnGraph(reads,k):
    dicti={}
    E=[]
    for read in reads:
        KMers=kmers(read,k)
        edges=[kmers(mer,k-1) for mer in KMers]
        for edge in edges:
            if edge[0] not in dicti.keys(): dicti[edge[0]]=[]
            if edge[1] not in dicti.keys(): dicti[edge[1]]=[]
            dicti[edge[0]].append(edge[1])
            E.append(edge)
    V=list(dicti.keys())
    graph={'nodes':V,'edges':E}
    #print(graph)
    return (graph,dicti)

def visualizeDBGraph(graph):
    dbGraph = networkx.DiGraph()
    dbGraph.add_nodes_from(graph['nodes']) #Add the nodes to the graph
    dbGraph.add_edges_from(graph['edges']) #Add the edges to the graph
    networkx.draw(dbGraph, with_labels=True, node_size=1000)
    plot.show()
  
    
graph,dicti=DeBruijnGraph(['TTACGTT','CCGTTA','GTTAC','GTTCGA','CGTTC'],5)
#graph,dicti=DeBruijnGraph(['TAATGCCATGGGATGTT'],3)
#graph,dicti=DeBruijnGraph(['ATGG', 'TGCC', 'TAAT', 'CCAT', 'GGG', 'GGATG', 'ATGTT'],3)    
#visualizeDBGraph(graph)
#print(dicti)


#[No. Of Nodes (out)] - [No. Of Nodes (in)]
Diff={}
for v in dicti.keys():  Diff[v]=len(dicti[v])
for v in dicti.keys():    
    for u in dicti[v]:  Diff[u]-=1
    
#print(Diff)

startNode =""
for i in Diff.keys():
    if(Diff[i] == 1):
        startNode = i

#Euler Path
path = []
def EulerPath(dicti,startNode):
    for i in dicti[startNode]:
          dicti[startNode].remove(i)
          EulerPath(dicti,i)
    path.append(startNode)

EulerPath(dicti,startNode)
path.reverse()
#print(path)

def getSequence(path):
    sequence = path[0]
    for i in range(1,len(path)):
       sequence += path[i][-1]
    return sequence

print(getSequence(path))
