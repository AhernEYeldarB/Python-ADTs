#   _____    _   _  U _____ u      ____     ____        _       ____    _   _          _      ____   _____
#  |_ " _|  |'| |'| \| ___"|/   U /"___|uU |  _"\ u U  /"\  u U|  _"\ u|'| |'|     U  /"\  u |  _"\ |_ " _|
#    | |   /| |_| |\ |  _|"     \| |  _ / \| |_) |/  \/ _ \/  \| |_) |/| |_| |\     \/ _ \/ /| | | |  | |
#   /| |\  U|  _  |u | |___      | |_| |   |  _ <    / ___ \   |  __/ U|  _  |u     / ___ \ U| |_| |\/| |\
#  u |_|U   |_| |_|  |_____|      \____|   |_| \_\  /_/   \_\  |_|     |_| |_|     /_/   \_\ |____/ u |_|U
#  _// \\_  //   \\  <<   >>      _)(|_    //   \\_  \\    >>  ||>>_   //   \\      \\    >>  |||_  _// \\_
# (__) (__)(_") ("_)(__) (__)    (__)__)  (__)  (__)(__)  (__)(__)__) (_") ("_)    (__)  (__)(__)_)(__) (__)

import graph.Vertex as Vertex
import graph.Edge as Edge
import graph.Stack
import copy
from math import radians, cos, sin, asin, sqrt


class Graph(object):
    '''
    Graph

    Params


    Methods:
        vertices(): return a list of all vertices
        edges(): return a list of all edges
        numVertices(): return the number of vertices
        numEdges(): return the number of edges
        getEdge(x,y): return the edge between x and y (if it exists)
        degree(x): return the degree of vertex x
        getEdges(x): return a list of all edges incident on x
        addVertex(elt): add a new vertex with element = elt
        addEdge(x, y, elt) a new edge between x and y, with element elt
        removeVertex(x): remove vertex and all incident edges
        removeEdge(e): remove edge e
    '''

    # Implemented as an adjacency map
    def __init__(self):
        self._vertices = {}
        self._inedges = {}
        self._v = {}
        self._numVertices = 0
        self._numEdges = 0

    def __str__(self):
        """ Return a string representation of the graph.

            Only represents the forward edges.
        """
        hstr = ('|V| = ' + str(self.numVertices()) + '; |E| = ' +
                str(self.numEdges()))
        vstr = '\nVertices: '
        for v in self._vertices:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    def vertices(self):
        return [key for key in self._vertices]
        # return list(self._vertices.keys())

    def numVertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._vertices)

    def getVertexByLabel(self, element):
        """ get the first vertex that matches element. """
        return self._v[element]

    def edges(self):
        edgelist = []
        for vertex in self._vertices:
            for edge in self._vertices[vertex]:
                # to avoid duplicates, only return out edges
                if self._vertices[vertex][edge].start() == vertex:
                    edgelist.append(self._vertices[vertex][edge])
        return edgelist

    def getEdges(self, v):
        """ Return a list of all (out) edges incident on v. """
        return self.getOutedges(v)

    def getOutedges(self, vertex):
        """ Return a list of all out edges from v. """
        if vertex in self._vertices:
            edgelist = []
            for edge in self._vertices[vertex]:
                edgelist.append(self._vertices[vertex][edge])
            return edgelist
        return None

    def numEdges(self):
        return self._numEdges

    def getEdge(self, vertex, edge):
        if (self._vertices != None and vertex in self._vertices
                and edge in self._vertices[vertex]):
            return self._vertices[vertex][edge]
        return None
        # return (self._vertices[a].getConnectingEdge(b))

    def degree(self, vertex):
        return len(self._vertices[vertex])
        # return a.getDegree()

    def outDegree(self, vertex):
        return len(self._vertices[vertex])

    def inDegree(self, vertex):
        return len(self._inedges[vertex])

    def addVertex(self, label, x=None, y=None):
        vertex = Vertex.Vertex(label, x, y)
        self._v[label] = vertex
        self._vertices[vertex] = dict()
        self._inedges[vertex] = dict()
        self._numVertices += 1
        return vertex

    def addVertex_if_new(self, label, x, y):
        """ Add and return a vertex with element, if not already in graph.

            Checks for equality between the elements. If there is special
            meaning to parts of the element (e.g. element is a tuple, with an
            'id' in cell 0), then this method may create multiple vertices with
            the same 'id' if any other parts of element are different.

            To ensure vertices are unique for individual parts of element,
            separate methods need to be written.
        """
        for vertex in self._vertices:
            if vertex.element() == label:
                #print('Already there')
                return vertex

        self._numVertices += 1
        return self.addVertex(label, x, y)

    def addEdge(self, vertexA, vertexB, label, weight, oneway='true'):
        """ Add and return an edge between two vertices v and w, with  element.

            If either v or w are not vertices in the graph, does not add, and
            returns None.
            
            If an edge already exists between v and w, this will
            replace the previous edge.
        """
        if not weight:
            weight = self._distance(vertexA, vertexB)
        # CHECK IS NOT NEEEDED FOR CURRENT DATA SET AS WE KNOW IT IS CORRECT
        # if not vertexA in self._vertices or not vertexB in self._vertices:
        #     return None

        if oneway == 'false':
            self.addEdge(vertexB, vertexA, label, weight)

        newEdge = Edge.Edge(vertexA, vertexB, label, weight)

        vertexA._outEdges[vertexB] = newEdge
        vertexB._inEdges[vertexA] = newEdge

        self._vertices[vertexA][vertexB] = newEdge
        self._inedges[vertexB][vertexA] = newEdge

        self._numEdges += 1
        return newEdge

    def _distance(self, vertexA, vertexB):
        ''' To calculate the the great circle distance
         between two points using haversines formula
         https://stackoverflow.com/questions/4913349/
         haversine-formula-in-python-bearing-and-distance-between-two-gps-points'''
        latA = vertexA._cords[0]
        lonA = vertexA._cords[1]
        latB = vertexB._cords[0]
        lonB = vertexB._cords[1]
        latA, lonA, latB, lonB = map(radians, [latA, lonA, latB, lonB])
        # Haversine formula
        dlon = lonB - lonA
        dlat = latB - latA
        a = sin(dlat / 2)**2 + cos(latA) * cos(latB) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles

        return (c * r)

    def addEdgePairs(self, edgelist):
        """ add all vertex pairs in elist as edges with empty elements. """
        for (vertexA, vertexB) in edgelist:
            self.addEdge(vertexA, vertexB, None, 0)

    def removeVertex(self, a):
        pass

    def removeEdge(self, e):
        pass

    #--------------------------------------------------#
    #Additional methods to explore the graph

    def highest_degreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._vertices:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv

    def highest_inDegreevertex(self):
        """ Return the vertex with highest in-degree. """
        hd = -1
        hdv = None
        for v in self._inedges:  #_vertices would also work for the loop
            if self.inDegree(v) > hd:
                hd = self.inDegree(v)
                hdv = v
        return hdv

    def highest_outDegreevertex(self):
        """ Return the vertex with highest out-degree. """
        return self.highest_degreevertex()

    def dfs_stack(self, v):
        """ Return a DFS tree from v, using a stack. """
        marked = {v: None}
        stack = Stack.Stack()
        stack.push(v)
        while stack.length() > 0:
            vertex = stack.pop()
            for e in self.getEdges(vertex):
                w = e.opposite(vertex)
                if w not in marked:
                    marked[w] = e
                    stack.push(w)
        return marked

    def depthfirstsearch(self, v):
        """ Return a DFS tree from v. """
        marked = {v: None}
        self._depthfirstsearch(v, marked)
        return marked

    def _depthfirstsearch(self, v, marked):
        """ Do a DFS from v, storing nodes in marked. """
        for e in self.getEdges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthfirstsearch(w, marked)

    def breadthfirstsearch(self, v):
        """ Return a BFS tree from v. """
        marked = {v: None}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.getEdges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = e
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def BFS_length(self, v):
        """ Return a BFS tree from v, with path lengths. """
        marked = {v: (None, 0)}
        level = [v]
        levelint = 1
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.getEdges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = (w, levelint)
                        nextlevel.append(x)
            level = nextlevel
            levelint += 1
        return marked

    def breadthfirstsearchtree(self, v):
        """ Return a down-directed BFS tree from v. """
        marked = {v: []}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.getEdges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = []
                        marked[w].append(x)
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def transitiveclosure(self):
        """ Return the transitive closure using version of FloydWarshall. """
        gstar = copy.deepcopy(self)
        vs = gstar.vertices()
        n = len(vs)
        for k in range(n):
            for i in range(n):
                if i != k and gstar.getEdge(vs[i], vs[k]) is not None:
                    for j in range(n):
                        if (i != j and k != j
                                and gstar.getEdge(vs[k], vs[j]) is not None):
                            if gstar.getEdge(vs[i], vs[j]) == None:
                                gstar.addEdge(vs[i], vs[j], 1)
        return gstar

##any vertex that has no in-edges, or only has in-edges from vertices
##        already added to the sort, can go next in the sort
## so:
##get a list of all vertices with 0 degree, and pick one
##check the vertices it points to.
##If any of them now have no more inedges, add them to the list
##pick another vertex from the list and repeat
##
##How can we check whether or not a vertex has 0 in-edges from non tsort vertices?
## - record the in-degree of each vertex
## - each time we add a vertex into tsort, go to each of its opposites,
##          and decrement their in-edge count
## - when a vertex count reduces to 0, add it to the list of available vertices

    def topological_sort(self):
        """ Return a list of the vertices of the graph in topological sort order.

            If the graph is not a DAG, return None.
        """
        inedgecount = {}  #map of v:id, where id is the number of inedges in
        #for v from vertices not in tsort
        tsort = []  #t-sorted list of vertices
        available = []  #list of vertices with no in-edges left from non tsort

        #initialise the inedgecount map
        for v in self._vertices:
            v_incount = self.inDegree(v)
            inedgecount[v] = v_incount
            if v_incount == 0:
                available.append(v)

        #repeat: take next available vertex, and append to tsort; update
        while len(available) > 0:
            w = available.pop()
            tsort.append(w)
            for e in self.getEdges(w):
                u = e.opposite(w)
                inedgecount[u] -= 1
                if inedgecount[u] == 0:
                    available.append(u)

        #if tsort is not same length as numVertices, return None
        print(tsort, self.numVertices())
        if len(tsort) == self.numVertices():
            return tsort
        else:
            return None

    #End of class definition


#---------------------------------------------------------------------------#
