# Implementation of Dijkstra's shortest path algortihm
import APQ as q
import Graph as g
'''
open starts as an empty APQ
locs is an empty dictionary (keys are vertices, values are location in open)
closed starts as an empty dictionary
preds starts as a dictionary with value for s = None
add s with APQ key 0 to open, and add s: (elt returned from APQ) to locs
while open is not empty
    remove the min element v and its cost (key) from open
    remove the entry for v from locs and preds (which returns predecessor)
    add an entry for v :(cost, predecessor) into closed
    for each edge e from v
        w is the opposite vertex to v in e
        if w is not in closed
            newcost is v's key plus e's cost
            if w is not in locs //i.e. not yet added into open
                add w:v to preds, add w:newcost to open,
                    add w:(elt returned from open) to locs
        else if newcost is better than w's oldcost
            update w:v in preds, update w's cost in open to newcost
return closed
'''


class PathFinder(object):
    def __init__(self, filename=None):
        if filename != None:
            self.setGraph(filename)

    def setGraph(self, filename):
        self._graph = self.graphreader(filename)

    def dijkstraShortestPath(self, start):
        openNodes = q.APQ()
        locations = {
        }  # Empty dict with keys as vertices, values are positions in open
        closedNodes = {}
        predecessors = {start: None}
        s = openNodes.add(0, start)
        locations[start] = s
        while not openNodes.isEmpty():
            v = openNodes.removeMin()
            k = v._key
            v = v._value
            locations.pop(v)
            pred = predecessors.pop(v)
            closedNodes[v] = (k, pred)

            for vertex in v._outEdges:
                # Iterating through vertices and not edges
                connectingEdge = v._outEdges[vertex]

                if vertex not in closedNodes:
                    newcost = k + connectingEdge._weight
                    if vertex not in locations:
                        predecessors[vertex] = v
                        temp = openNodes.add(newcost, vertex)
                        locations[vertex] = temp

                    elif newcost < locations[vertex]._key:
                        predecessors[vertex] = v
                        elem = locations[vertex]
                        openNodes.updateKey(elem, newcost)

        return closedNodes

    def graphreader(self, filename):
        """ Read and return the route map in filename. """
        ''' 
        File Format:
            Node
            id: 1495685415 #Vertex Label
            gps: 12.9688948 -4.6395383 #GPS Co-ords

            Edge
            from: 349067617 # Vertex from
            to: 349067618   # Incident Vertex
            length: 0.011789063681904651 # Distance
            time: 1.414687641828558 # Weight in this instance
            oneway: false # Creates a second edge in the other direction
        '''

        graph = g.Graph()
        file = open(filename, 'r')
        entry = file.readline()  #either 'Node' or 'Edge'
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            gps = file.readline().split()  # Skip gps data for now
            vertex = graph.addVertex(nodeid, gps[1], gps[2])
            entry = file.readline()  #either 'Node' or 'Edge'
        print('Read', num, 'vertices and added into the graph')
        num = 0

        while entry == 'Edge\n':
            num += 1
            source = int(file.readline().split()[1])
            sv = graph.getVertexByLabel(source)
            target = int(file.readline().split()[1])
            tv = graph.getVertexByLabel(target)
            # length = float(file.readline().split()[1])
            file.readline()
            time = float(file.readline().split()[1])
            way = file.readline().split()[1]  #read the one-way data
            edge = graph.addEdge(sv, tv, None, time, way)  #edge =
            entry = file.readline()  #either 'Node' or 'Edge'
            # print('source:%s target:%s'%(source, target))

        print('Read', num, 'edges and added into the graph')
        return graph

    def shortestPath(self, v, w):
        v = self._graph.getVertexByLabel(v)  # v = Start
        w = self._graph.getVertexByLabel(w)  # w = End

        allPaths = self.dijkstraShortestPath(v)

        print('type\t,latitude\t,longitude\t,element\t,cost')
        time, prev = allPaths[w]
        print('W\t,%s\t,%s\t,%s\t,%s' % (w._cords[0], w._cords[1], w.element(),
                                         time))
        while allPaths[prev][1] != v:
            # path.append(prev)
            time, prev = allPaths[prev]
            print('W\t,%s\t,%s\t,%s\t,%s' % (prev._cords[0], prev._cords[1],
                                             prev.element(), time))

    def Main(self, start, end):
        # List of locattions
        # ids = {

        # Start, end
        sourcestr = start
        deststr = end

        # Print shortest path
        self.shortestPath(sourcestr, deststr)


if __name__ == '__main__':
    f = ''  #Filename
    graph = PathFinder()
    graph.setGraph(f)

    NodeA = 0
    NodeB = 0
    graph.Main(NodeA, NodeB)
