class Edge(object):
    '''
    Edge:
        Representation of an Edge object in a graph ADT which connects two vertices together.

        Params:
        @param@ label = the name or label of the edge
        @param@ vertexA = One of the incident vertices, the source vertex for an ordere graph
        @param@ vertexB = The other, incident vertex.

        Methods:
        vertices(): returns the pair of vertices the edge is incident on. Stored as a tuple so is an ordered pair for directed graphs
        opposite(x): if the edge is incident on x, return the other vertex
        element(): return the label of the edge
    '''

    def __init__(self, vertexA, vertexB, label, weight=0):
        if label == None:
            self._label = str(vertexA.element()) + '--' + str(vertexB.element())
        else:
            self._label = label
        self._weight = weight
        self._vertices = (vertexA, vertexB)

    def __repr__(self):
        outstring = ('%s: ' % (self._label))
        return outstring
        
    def __str__(self):
        # return ('(' + str(self._vertices[0]) + '--'
        #     + str(self._vertices[1]) + ' : '
        #     + str(self._label) + ')')
        return ('(' + str(self._label) +' : ' + str(self._weight) + ')')

    def vertices(self):
        return self._vertices

    def opposite(self, x):
        if self._vertices[0] == x:
            return self._vertices[1]

        elif self._vertices[1] == x:
            return self._vertices[0]

    def start(self):
        return self._vertices[0]

    def end(self):
        return self._vertices[1]

    def element(self):
        return self._label