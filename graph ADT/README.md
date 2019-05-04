GraphADT
My implementation of a Graph ADT in python. Consisting of an Edge, Vertex and Graph class.

Specifications from: http://www.cs.ucc.ie/~kb11/teaching/CS2516/Lectures/restricted/L10-TheGraphADT.pdf

Vertex element(): returns the label of the vertex

Edge vertices(): returns the pair of vertices the edge is incident on opposite(x): if the edge is incident on x, return the other vertex element(): return the label of the edge

(directed) Graph ADT vertices(): return a list of all vertices edges(): return a list of all edges num_vertices(): return the number of vertices num_edges(): return the number of edges get_edge(x,y): return the edge between x and y (if it exists) degree(x): return the degree of vertex x get_edges(x): return a list of all edges incident on x add_vertex(elt): add a new vertex with element = elt add_edge(x, y, elt) a new edge between x and y, with element elt remove_vertex(x): remove vertex and all incident edges remove_edge(e): remove edge e