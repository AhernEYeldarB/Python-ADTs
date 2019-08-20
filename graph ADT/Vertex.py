# print(r'''
# ██╗   ██╗███████╗██████╗ ████████╗███████╗██╗  ██╗
# ██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
# ██║   ██║█████╗  ██████╔╝   ██║   █████╗   ╚███╔╝
# ╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝   ██╔██╗
#  ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██╔╝ ██╗
#   ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
# ''')


class Vertex():
    '''
    Vertex:
        Representation of a vertex object for a Graph ADT

        Params:
            @param@ label = The name or label for the graph (Ie the element it represents)

        Methods:
            element(): Returns the vertex label
            addAdjacent(b, e): Adds an edge to be incident on a vertex 
            getAdjacentVertices(): Returns a list of incident edges 
    '''
    __slots__ = ['_label','_name','_cords','_inEdges', '_outEdges','_tags']
    def __init__(self, label, x, y, name=None):
        self._label = label
        self._name = name
        # Used if vertex represents a location on a map
        self._cords = (x, y)
        # Dictionary of edgdes incident on this vertex
        self._inEdges = {}
        self._outEdges = {}
        self._tags = {}
        # self._degree = 0

    def __repr__(self):
        outstring = ('%s: ' % (self._label))
        return outstring
        # outstring = self._label
        # return str(outstring)

    def __str__(self):
        # if self._name:
        #     return self._name
        return str(self._label)

    def element(self):
        # Return the label of the vertex
        # if self._name:
        #     return self._name

        return str(self._label)
        # return self._label

    # def getDegree(self):
    #     # Returns the number of edges incident on the vertex
    #     return self._degree