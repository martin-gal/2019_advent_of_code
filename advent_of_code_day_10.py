# Advent of Code - Day 10
from math import gcd

# Daten einlesen
with open('d:/42_python/aoc_data/day_10.txt', 'r', ) as f:
    aoc_input = f.read().splitlines()


zeilen = len(aoc_input)
spalten = len(aoc_input[0])

# Lege die Karte als Dictonary an, wobei die Koordinaten die Einträge sind
katalog = dict()
koor_ast = list()
for z in range(0, zeilen):
    for s in range(0, spalten):
        eintrag = dict()
        eintrag['#'] = True if aoc_input[s][z] == '#' else False
        eintrag['Wert'] = 0
        katalog[(z, s)] = eintrag
        koor_ast.append((z, s)) if aoc_input[s][z] == '#' else False


# Teil 1: finde den Asteroid, von dem man die meisten anderen aus sehen kann.
# 
# [X] Ansatz: Erzeuge eine Liste von Koordinaten der Asterioden
# [X] wähle einen Asteroiden
# [X] streiche den aktuellen Asterioden aus dieser Liste
# [X] laufe die Liste ab. Nimm den ersten Asterioden (c,d)
# [X] Berechne daraus die Schrittweite (c,d) - (a,b) zu diesem Asterioden und kürze diese mit dem
# [X] ggT (gcd()) => Schrittweite (x,y)
# [X] Beginnend von dem Startpunkt (a,b) addiere n*(x,y) n=1,...,m so lange, bis a+x oder b+y außerhalb des Bildes
# [X] liegt oder ein Asteriod getroffen wurde.
# [X] Wenn ein Asteroid (mit Koordinate (a,b) + r*(x,y)) getroffen wurde, erhöhe den Wert des Startpunktes um 1.
# [X] entferne den Asteroid und alle Asteroiden mit Koordinaten (a,b) + s*(x,y) aus der Liste, mit s > r.
def teil_1():
    for ast in koor_ast:
        tmp_ast = koor_ast.copy()       # Kopie der Asteroiden-Liste
        tmp_ast.remove(ast)             # Entferne den aktuellen Asteroiden
        while tmp_ast:
            betrachter = tmp_ast.pop()
            katalog[ast]['Wert'] += 1                # Ein Asteriod ist damit mindestens sichtbar
            # schrittweite = tuple(map(sum, zip(a, b)))     # funktioniert leider nicht, da Subtraktion notwendig
            schrittweite = tuple(item1 - item2 for item1, item2 in zip(betrachter, ast))
            ggT = gcd(schrittweite[0], schrittweite[1])
            schrittweite = (schrittweite[0] / ggT, schrittweite[1] / ggT)
            ziel = tuple(map(sum, zip(ast, schrittweite)))
            while (0 <= ziel[0] < zeilen) and (0 <= ziel[1] < spalten):
                tmp_ast.remove(ziel) if ziel in tmp_ast else False
                ziel = tuple(map(sum, zip(ziel, schrittweite)))
    ausgabe = [(ast, katalog[ast]['Wert']) for ast in koor_ast]
    print(max(ausgabe, key=lambda t: t[1]))


teil_1()  # Lösung: 260


# Teil 2: Zerstöre Asteroiden mit einem Laser.
# Der Laser beginnt nach oben gerichtet und rotiert im Uhrzeigersinn.
# Welches ist der 200. Asteroid, der zerstört wird? Lösung: x-Koordinate + 100 * y-Koordinate
# TODO  Rotation des Lasers überlegen
#       (r * sin(phi), r * cos(phi))
def teil_2():
    zaehler = 0
    richtung = (0, 1)

