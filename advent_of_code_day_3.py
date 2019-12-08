# Advent of Code - Day 3
# Teil 1
# Finde den Schnittpunkt von zwei Kabeln

# Daten importieren
import csv
with open('d:/42_python/aoc_data\day_3_1.csv') as f:
    aoc_day_3 = [rec for rec in csv.reader(f, delimiter=',')]

print(aoc_day_3)

# Schreibe die Eckpunkte des Graphen in eine Liste
graph_1 = [(0,0)]
graph_2 = [(0,0)]

# Erzeuge zwei Listen, die alle Punkte enthalten, die von den Kabeln abgelaufen werden
# Bilde die Schnittmenge dieser Listen
for i in range(2):
    for beweg in aoc_day_3[i]:
        weg = int(beweg[1:])
        for j in range(1, weg + 1):
            if beweg[0][0] == 'R':
                if i == 0:
                    graph_1.append(tuple(map(sum, zip(graph_1[-1], (1, 0)))))
                else:
                    graph_2.append(tuple(map(sum, zip(graph_2[-1], (1, 0)))))
            elif beweg[0][0] == 'L':
                if i == 0:
                    graph_1.append(tuple(map(sum, zip(graph_1[-1], (-1, 0)))))
                else:
                    graph_2.append(tuple(map(sum, zip(graph_2[-1], (-1, 0)))))
            elif beweg[0][0] == 'U':
                if i == 0:
                    graph_1.append(tuple(map(sum, zip(graph_1[-1], (0, 1)))))
                else:
                    graph_2.append(tuple(map(sum, zip(graph_2[-1], (0, 1)))))
            elif beweg[0][0] == 'D':
                if i == 0:
                    graph_1.append(tuple(map(sum, zip(graph_1[-1], (0, -1)))))
                else:
                    graph_2.append(tuple(map(sum, zip(graph_2[-1], (0, -1)))))
schnittpunkte = list(set(graph_1).intersection(graph_2))
schnittpunkte.remove((0,0)) # Der Startpunkt soll nicht mitgezählt werden
# Der Manhatten-Grid-Abstand benötigt die absoluten Koordinaten
ausgabe_2 = list(tuple(map(abs, punkte)) for punkte in schnittpunkte)
ausgabe_2 = list(sum(punkte) for punkte in ausgabe_2)
print(schnittpunkte)
print(min(ausgabe_2)) # Lösung 207

# Teil 2: finde den Schnittpunkt, der nach den wenigsten Schritten erreicht wird
index = []
for punkte in schnittpunkte:
    index.append(graph_1.index(punkte) + graph_2.index(punkte))

print(min(index)) # Lösung 21196