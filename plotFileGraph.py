import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz
from collections import defaultdict

class Graph():
    def __init__(self):
        #empty defaultDict
        #empty valuemap dicitonary
        self.edges = defaultdict(list)
        self.val_map = {}

    #adds an edge to the graph
    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)

    #adds the value map
    def add_val_map(self, val_map):
        self.val_map = val_map

    def print_ordered_file_structure(self, start):
        # Mark all the vertices as not visited 
        visited = defaultdict(bool)
  
        # Create a stack for BFS 
        stack = [] 
  
        # Mark the source node as  
        # visited and remove it 
        stack.append(start) 
        visited[start] = True
  
        while stack: 
            # Dequeue a vertex from  
            # queue and print it 
            start = stack.pop() 
            f = open("output.txt", "a")
            f.write(start+'. ' + self.val_map[start] + '\n')
            f.close()
            #print (start+'. ', self.val_map[start]) 
            # Get all adjacent vertices of the 
            # removed vertex s. If a adjacent 
            # has not been visited, then mark it 
            # visited and append it
            # makes a list, sorts it, and reverses it
            # so it can be printed in order
            lst = self.edges[start]
            lst.sort()
            lst = lst[::-1]
            for j in lst:
                if visited[j] == False: 
                    stack.append(j) 
                    visited[j] = True
            

#reads the file
#parameters: list of edges, dictionary of nodes and values
def readFile(edges, val_map):
    
    #opens the file for reading
    readFile = open("textOutlineOmit.txt", "r")

    #for every line extract the edge and the value
    for line in readFile:
        dirAndVal = line.split(". ")
        dirAndVal[1] = dirAndVal[1].strip()

        #checks that it is not "0"
        if(dirAndVal[0] != "0"):
            aTuple = (dirAndVal[0][:-1], dirAndVal[0])
            edges.append(aTuple)
        val_map[dirAndVal[0]] = dirAndVal[1]

    #closes the file
    readFile.close()

#draws the graph using networkx
def drawGraph(G, val_map):

    #uses this funciton to generate the pos
    pos = hierarchy_pos(G,"0")
    nx.draw(G, pos = pos, with_labels=False)
    nx.draw_networkx_labels(G, pos, val_map, 4)
    plt.show()

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike
    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.
    G: the graph (must be a tree)
    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.
    width: horizontal space allocated for this branch - avoids overlap with other branches
    vert_gap: gap between levels of hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments
        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed
        '''
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
        
def main():
    #empty list for edges
    edges = []
    #empty dictionary for value map
    val_map = {}
    #reads the file
    readFile(edges, val_map)

    #displaying the graph with networkx
    G = nx.DiGraph()
    G.add_edges_from(edges)
    drawGraph(G, val_map)

    #printing the contents in order
    #initializes graph object
    #adds the edges one by one
    #adds the val_map
    #prints the structure similar to
    # the input file
    G2 = Graph()
    for edge in edges:
        G2.add_edge(*edge)
    G2.add_val_map(val_map)
    G2.print_ordered_file_structure("0")
    
main()
