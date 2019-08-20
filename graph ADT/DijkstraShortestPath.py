# Implementation of Dijkstra's shortest path algortihm
# Author Bradley Aherne

import graph.APQ as q
import graph.Graph as g
import graph.GraphBuilder
# import requests
from sys import argv
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
            self.buildFromOSM(filename)
        else:
            self._graph = g.Graph()
            # self.buildFromTxt()

    def buildFromOSM(self, filename):
        # Builds the graph from an OSM file
        print(filename)
        builder = GraphBuilder.GraphBuilder()
        builder.graphReaderOSM(filename)
        self._graph = builder._graph

    def buildFromTxt(self):
        # Builds the graph from a preparsed OSM Edge and vertex file
        with open('vertices.txt', 'r') as vertices:
            count = 0
            for line in vertices:
                data = line.split()
                nodeid = int(data[0])
                latitude = float(data[1])
                longitude = float(data[2])
                name = str(data[3:])
                vertex = self._graph.addVertex(nodeid, latitude, longitude)
                vertex._name = name
                count += 1

        print('Read All Vertices: %d' % (count))

        with open('edges.txt', 'r') as edges:
            count = 0
            for line in edges:
                data = line.split()
                edgeid = int(data[0])
                name = str(data[1:-4])
                distance = float(data[-3])  # In km
                A = self._graph.getVertexByLabel(int(data[-2]))
                B = self._graph.getVertexByLabel(int(data[-1]))

                edge = self._graph.addEdge(A, B, edgeid, None)
                edge._name = name
                count += 1

        print('Read all Edges: %d' % (count))
        # print(self._graph.getEdges())

    def buildFromDB(self, connection):
        # Built from a gtfs feed stored in a postgres database
        cursor = connection.cursor()
        
        query = 'SELECT stop.id, ST_x(stop.point), ST_Y(stop.point), stop.name FROM stop WHERE feed_id=1'

        cursor.execute(query)

        stops = cursor.fetchall()
        # count = 0
        for stop in stops:
            sid = stop[0]
            x = stop[1]
            y = stop[2]
            name = stop[3]
            vertex = self._graph.addVertex(sid, x, y)
            vertex._name = name
            # count += 1

        # print('added %d vertices into the graph' %(count))

        query = 'SELECT stop_time.id, stop_time.shape_dist_traveled, stop_time.stop_id, stop_time.trip_id, ST_X(stop.point), ST_Y(stop.point), trip.trip_id , trip.route_id, stop.name FROM stop_time INNER JOIN stop ON stop.id = stop_time.stop_id INNER JOIN trip ON trip.id = stop_time.trip_id order by stop_time.id;'
        cursor.execute(query)

        data = cursor.fetchone()
        while data:
            if data == None:
                break
            result = []
            distance = data[1]
            stop_id = data[2]
            tid = data[3]
            stopY = data[4]
            stopX = data[5]
            name = data[6]
            result.append(data)
    
            while True:
                data = cursor.fetchone()        
                if data == None:
                    break

                if data[3] != result[0][3]:
                    break 

                distance = data[1]
                stop_id = data[2]
                trip_id = data[3]
                stopY = data[4]
                stopX = data[5]
                name = data[6]
                result.append(data)

            for i in range(len(result)-1):
                vertexa = result[i]
                vertexb = result[i+1]
                
                A = self._graph.getVertexByLabel(vertexa[2])
                B = self._graph.getVertexByLabel(vertexb[2])
                edge = self._graph.addEdge(A, B, vertexa[0], vertexb[1]-vertexa[1])
                edge._name = trip_id
                
        print('Adding %s Vertices into the graph.'%(self._graph.numVertices()))
        print('Adding %s Edges into the graph.'%(self._graph.numEdges()))

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
        entry = file.readline()  # either 'Node' or 'Edge'
        num = 0
        while entry == 'Node\n':
            num += 1
            nodeid = int(file.readline().split()[1])
            gps = file.readline().split()  # Skip gps data for now
            vertex = graph.addVertex(nodeid, gps[1], gps[2])
            entry = file.readline()  # either 'Node' or 'Edge'
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
            way = file.readline().split()[1]  # read the one-way data
            edge = graph.addEdge(sv, tv, None, time, way)  # edge =
            entry = file.readline()  # either 'Node' or 'Edge'
            # print('source:%s target:%s'%(source, target))

        print('Read', num, 'edges and added into the graph')
        return graph

    def shortestPath(self, v, w):
        # Implement to get the node from coords
        v = self._graph.getVertexByLabel(v)  # v = Start
        w = self._graph.getVertexByLabel(w)  # w = End

        allPaths = self.dijkstraShortestPath(v)

        return allPaths

    def getPath(self, allPaths, destinationNodes):
        paths = {}
        for node in destinationNodes:    
            path = []
            weight, prev = allPaths[w]
            path.append( [w._cords[0], w._cords[1], w.element(), weight] )

            while allPaths[prev][1] != v:
                weight, prev = allPaths[prev]
                path.append( [prev._cords[0], prev._cords[1], prev.element(), weight ] )
            paths[node] = path
        return paths

    def toFile(self, allPaths)
    # allpaths dict object
        print(len(allPaths) )
        print('type\t,latitude\t,longitude\t,element\t,cost')
        with open('shortestPath.txt', 'w+') as outfile:
            time, prev = allPaths[w]
            # print('W\t,%s\t,%s\t,%s\t,%s' %
            #       (w._cords[0], w._cords[1], w.element(), time))
            outfile.write('%s, %s, %s, %s'% (w._cords[1], w._cords[0], w._name, w._label))
            outfile.write('\n')

            while allPaths[prev][1] != v:
                # path.append(prev)
                time, prev = allPaths[prev]
                # print('W\t,%s\t,%s\t,%s\t,%s' %
                #       (prev._cords[0], prev._cords[1], prev.element(), time))

                outfile.write('%s, %s, %s, %s' % (prev._cords[1], prev._cords[0], prev._name, prev._label))
                outfile.write('\n')

        print('path written to shortestPath.txt')

    def __call__(self, start, end):
        # Start, end
        sourcestr = start
        deststr = end

        # Print shortest path
        return self.shortestPath(sourcestr, deststr)


if __name__ == '__main__':
    f = '' # filename

    nodeA = 534442374  
    nodeB = 534442397 
    # nodeA = 2734957290
    # nodeB = 1925516316
    
    
    	
    graph = PathFinder(f)
    graph(nodeA, nodeB)
