# Advent of Code - Day 6
# import csv
#
# with open('d:/42_python/aoc_data/day_6.csv') as f:
#     aoc_input = list(csv.reader(f, delimiter='\n'))

with open('d:/42_python/2019_aoc/aoc_data/day_6.csv', 'r', ) as f:
    aoc_input = f.read().splitlines()

print(aoc_input)

# Teil 1
# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the
# download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct
# orbits (like the one shown above) and indirect orbits.
input_teil_1 = aoc_input.copy()

# Knoten- und Kantenmenge bestimmen
edges = list()
nodes = set()
for orbit in input_teil_1:
    carry = orbit.split(')')
    edges.append(carry)
    nodes.add(carry[0])
    nodes.add(carry[1])

# print(f"Kanten: {edges}\nKnoten: {nodes}")
#
# g_edge = dict()
# for node in nodes:
#     g_edge[node] = []
#     for edge in edges:
#         if node == edge[0]:
#             g_edge[node].append(edge[1])
#
# print("Graph mit Kanten:", g_edge)

# Erzeuge zu jedem Knoten einen Eintrag mit den Kindern
# Initialisiere die Distanz mit 0
g_tree = dict()
for node in nodes:
    g_tree[node] = dict()
    g_tree[node]['kind'] = []
    g_tree[node]['distanz'] = 0
    for edge in edges:
        if node == edge[0]:
            g_tree[node]['kind'].append(edge[1])


print("Graph mit Kindern: ", g_tree)


# Berechnet die Checksumme eines Graphen mit gegebener Wurzel
# Die Distanzen im Graphen müssen die Distanzen zur Wurzel sein
def chksum(graph):
    # i = - len(graph) * graph[wurzel]['distanz']
    i = 0
    for k in graph:
        i += graph[k]['distanz']
    return i


# Durchlaufe den Graphen und schreibe zu jedem Knoten die Distanz zur Wurzel
def dist(graph, start='COM', distanz=0):
    if graph[start]['kind']:
        for nachbar in graph[start]['kind']:
            graph[nachbar]['distanz'] = distanz + 1
            dist(graph, nachbar, distanz + 1)
    else:
        graph[start]['distanz'] = distanz
    return graph


g_tree = dist(g_tree)
print(f"{chksum(g_tree)}\n******************")  # Lösung = 261306

# Teil 2
# Kürzester Weg (die wenigsten Orbital-Transfers) zwischen mir (YOU) und Santa (SAN)
input_teil_2 = aoc_input.copy()

# Knoten- und Kantenmenge bestimmen
edges = list()
nodes = set()
for orbit in input_teil_2:
    carry = orbit.split(')')
    edges.append(carry)
    nodes.add(carry[0])
    nodes.add(carry[1])


# Initialisiere den Graphen
g_tree_2 = dict()
for node in nodes:
    g_tree_2[node] = dict()
    g_tree_2[node]['kind'] = []
    g_tree_2[node]['verbindung'] = set()
    for edge in edges:
        if node == edge[0]:
            g_tree_2[node]['kind'].append(edge[1])


# Prüfe, ob ein bestimmter Startknoten einen bestimmten Zielknoten erreichen kann
# gibt die Anzahl der Schritte zurück und schreibt in den Graphen als Verbindung den Zielknoten
def erreicht_knoten(graph, start, ziel):
    if start == ziel:
        graph[start]['verbindung'].add(ziel)
        return 0
    else:
        for nachbar in graph[start]['kind']:
            a = erreicht_knoten(graph, nachbar, ziel)
            if ziel in graph[nachbar]['verbindung']:
                graph[start]['verbindung'].add(ziel)
                return a + 1


# gesucht ist die minimale Strecke
# zwei Schritte müssen abgezogen werden, da der Startpunkt und der Endpunkt keine Schritte auslösen
zaehler = float('Inf')
for node in g_tree_2:
    dis_san = erreicht_knoten(g_tree_2, node, 'SAN')
    dis_you = erreicht_knoten(g_tree_2, node, 'YOU')
    if dis_san is not None and dis_you is not None and (dis_san + dis_you - 2 < zaehler):
        zaehler = dis_san + dis_you - 2

print(zaehler)  # Lösung 382

