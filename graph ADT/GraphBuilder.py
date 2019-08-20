import graph.Graph
import re
from sys import argv
import psycopg2


class GraphBuilder(object):
    def __init__(self):
        '''
            Build the graph from a .OSM file
        '''
        # Initialise graph
        # Build graph
        self._graph = Graph.Graph()

    # def graphReaderOSMDB(self, dbLogin):

    #     connection = psycopg2.connect(host=dbLogin[0], database=dbLogin[1], user=dbLogin[2],
    #                                   password=dbLogin[3])
    #     cursor = connection.cursor()

    #     # Get all nodes into Graph
    #     # id, version, user_id, tstamp, changeset_id ,tags, geom
    #     cursor.execute('SELECT id, tags, ST_Y(geom), ST_X(geom) FROM nodes;')
    #     result = cursor.fetchall()
    #     count = 0
    #     for data in result:
    #         nodeid = data[0]
    #         tags = data[1]
    #         latitude = data[2]
    #         longitude = data[3]
    #         Vertex = self._graph.addVertex(nodeid, latitude, longitude)
    #         count += 1
    #     print('Added %d vertices to the graph' %(count))

    #     # Add all ways/edges

    def graphReaderOSM(self, filename):
        '''
            Read in OSM filetype and build the adjacency Map
        '''
        '''
        osmosis script
        osmosis --read-pbf ireland-and-northern-ireland.osm.pbf --tf accept-ways highway=* --used-node --write-xml 0highways.osm
        '''
        '''
            File Format:
            <?xml version='1.0' encoding='UTF-8'?>
            <osm version="0.6" generator="Osmosis 0.47">
            <bounds minlon="" minlat="" maxlon="" maxlat="" origin="uri"/>

            ...
            <node id="" version="" timestamp="YYYY-DD-MMTHH:MM:SSZ"
             uid="" user="" changeset="" lat="" lon="">
            ...
            
            <relation> 
            <way>

        '''

        with open(filename, 'r', encoding='utf-8') as file:
            file.readline()  # XML Version and encoding
            file.readline()  # OSM Version and Generator
            file.readline()  # Bounds of Data (Polygon)
            entry = file.readline()
            count = 0

            # regex to pick out integer data
            gpsRegex = re.compile('\"(.*?)\"')

            # Finds all nodes first
            with open('vertices.txt', 'w+') as verts:
                while '<way' not in entry:
                    if '<node' in entry:
                        info = entry.split()
                        # print(info)
                        nodeid = int(
                            gpsRegex.search(info[1]).group().strip('\"'))
                        lat = float(
                            gpsRegex.search(info[-2]).group().strip('\"'))
                        lon = float(
                            gpsRegex.search(info[-1]).group().strip('\"'))
                        # print(nodeid, lat, lon)
                        vertex = self._graph.addVertex(nodeid, lat, lon)
                        count += 1

                    if '<tag k=\"name\"' in entry:
                        info = entry.split()
                        # print(gpsRegex.search(''.join(info[1:-1])).group().strip('\"'))
                        name = info[2:]
                        outstr = ' '
                        outstr = outstr.join(name)
                        # print(gpsRegex.search(outstr).group().strip('\"'))
                        name = gpsRegex.search(outstr).group().strip('\"')
                        vertex._name = name
                    entry = file.readline()

                vertices = self._graph.vertices()
                for vertex in vertices:
                    verts.write('%s\t%s\t%s\t%s\n' %
                                (vertex._label, vertex._cords[0],
                                 vertex._cords[1], vertex._name))

                print('Read', count, 'Vertices into the graph')

            with open('edges.txt', 'w+') as edges:
                count = 0
                while '<way' in entry:
                    nodes = []
                    info = entry.split()
                    wayid = gpsRegex.search(info[1]).group()
                    entry = file.readline()
                    while '<nd' in entry:
                        count += 1
                        source = int(
                            gpsRegex.search(entry).group().strip('\"'))
                        entry = file.readline()
                        target = gpsRegex.search(entry).group().strip('\"')
                        # print('source ', source)
                        # print('target ', target)
                        if target.isdigit():
                            target = int(target)
                            sv = self._graph.getVertexByLabel(source)
                            tv = self._graph.getVertexByLabel(target)
                            edge = self._graph.addEdge(sv, tv, None, None)
                    else:
                        while '<way' not in entry:
                            if not entry:
                                break
                            elif '<tag k=\"name\"' in entry:
                                info = entry.split()
                                # print(gpsRegex.search(''.join(info[1:-1])).group().strip('\"'))
                                name = info[2:]
                                outstr = ' '
                                outstr = outstr.join(info[2:])
                                outstr = gpsRegex.search(outstr).group().strip(
                                    '\"')
                                edge._name = outstr
                            entry = file.readline()

                        # label, name, distance(weight), vertexA, VertexB
                        # print('%s\t%s\t%s\t%s\t%s\n' %
                        #       (hash(edge._label), edge._name, edge._weight,
                        #        edge._vertices[0], edge._vertices[1]))

                        edges.write(
                            '%s\t%s\t%s\t%s\t%s\n' %
                            (hash(edge._label), edge._name, edge._weight,
                             edge._vertices[0], edge._vertices[1]))

                    if not entry:
                        break

            print('Read', count, 'Edges into the graph')


if __name__ == '__main__':
    # Osm file to build graph

    flag = argv[1]
    if flag == '-f':
        file = argv[2]
        builder = GraphBuilder().graphReaderOSM(file)
    elif flag == '-d':
        login = argv[2:]
        print(login)
        builder = GraphBuilder().graphReaderOSMDB(login)

    print('Built graph')
