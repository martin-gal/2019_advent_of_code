# Advent of Code - Day 6
# import csv
#
# with open('d:/42_python/aoc_data/day_6.csv') as f:
#     aoc_input = list(csv.reader(f, delimiter='\n'))

with open('d:/42_python/aoc_data/day_6_test.csv', 'r', ) as f:
    aoc_input = f.read().splitlines()

print(aoc_input)

# Teil 1
# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the
# download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct
# orbits (like the one shown above) and indirect orbits.
input_teil_1 = aoc_input.copy()

# Knotenmenge bestimmen
nodes = list()
for orbit in input_teil_1:
    nodes.append(orbit.split(')'))

print(nodes)

graph = dict()
for node in nodes:
    graph[node[0]] = []
    for neighbour in nodes:
        if node[0] == neighbour[0]:
            graph[node[0]].append(neighbour[1])

print(graph)

graph = dict()
for node in nodes:
    graph[node[0]] = dict()
    graph[node[0]]['nachbar'] = []
    for neighbour in nodes:
        if node[0] == neighbour[0]:
            graph[node[0]]['nachbar'].append(neighbour[1])

# Die Distanzen müssen berechnet werden.
# TODO in dem Dictonary abspeichern; von unten nach oben summieren.
print(graph)

# graph2 = { "a" : ["c"],
#           "b" : ["c", "e"],
#           "c" : ["a", "b", "d", "e"],
#           "d" : ["c"],
#           "e" : ["c", "b"],
#           "f" : []
#         }
#
# def generate_edges(graph):
#     edges = []
#     for node in graph:
#         for neighbour in graph[node]:
#             edges.append((node, neighbour))
#
#     return edges
#
# print(generate_edges(graph2))