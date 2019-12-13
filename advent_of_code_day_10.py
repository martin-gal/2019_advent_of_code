# Advent of Code - Day 10
from math import gcd
import math

# Daten einlesen
with open('d:/42_python/2019_aoc/aoc_data/day_10.txt', 'r', ) as f:
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
        tmp_ast = koor_ast.copy()  # Kopie der Asteroiden-Liste
        tmp_ast.remove(ast)  # Entferne den aktuellen Asteroiden
        while tmp_ast:
            betrachter = tmp_ast.pop()
            katalog[ast]['Wert'] += 1  # Ein Asteriod ist damit mindestens sichtbar
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


# teil_1()  # Lösung: 260


# Teil 2: Zerstöre Asteroiden mit einem Laser.
# Ausgangspunkt ist das Ergebnis aus Teil 1: (14, 17)
# Der Laser beginnt nach oben gerichtet und rotiert im Uhrzeigersinn.
# Welches ist der 200. Asteroid, der zerstört wird? Lösung: x-Koordinate + 100 * y-Koordinate
# [O]   Rotation des Lasers überlegen
#       (r * sin(phi), r * cos(phi))
#       Die Schrittweite muss so gewählt sein, dass nicht zwei hintereinander liegende Felder getroffen werden
# [X]   Die Steigungen zu allen Asteroiden berechnen (von inf über 0 bis - inf; Halbebenen beachten)
# [X]   Sortiere nach Steigung, wenn mehrere die gleiche Steigung haben, dann nach Entfernung gegeben durch
#       euklidischen Abstand math.sqrt((x-a)**2 + (y-b)**2)
#       Beachte die Halbebenen und erzeuge eine sortierte Liste von Elementen, die abgearbeitet werden können
# [X]   Beginne auf rechter Halbebene
#       Suche Asteroiden mit kleinster Steigung und kürzester Entfernung.
#       Gib seine Daten aus.
#       Entferne den Asteroiden
# [X]   Suche den nächsten Asteroiden (im Quadranten 1) mit der nächsten Steigung (d.h.  > als die aktuell betrachtete)
#       Entferne den Asteroiden mit der kürzensten Entfernung.
# [X]   Wenn es keinen Asteroiden mehr im Quadranten 1 gibt, gehe zu 2.
#       --> Wenn Steigung inf erreicht ist, wechsle in die linke Halbebene und nimm fallende Steigungen
def teil_2(basis=(14, 17)):
    lst_roid_r = []
    lst_roid_l = []
    lst_slop_r = set()
    lst_slop_l = set()
    tmp_ast = koor_ast.copy()
    tmp_ast.remove(basis)
    for ast in tmp_ast:
        m, q = slope(ast, basis)
        # Koordinate, Steigung, Entfernung
        # Der Abstand auf der linken HE wird negativ ausgewiesen, um das Sortieren zu ermöglichen
        if q in [1, 2]:
            lst_roid_r.append((ast, m, norm2(ast, basis), True))
            lst_slop_r.add(m)
        else:
            lst_roid_l.append((ast, m, -norm2(ast, basis), False))
            lst_slop_l.add(m)
    # Sortiere die Liste aufsteigend (lst_roid nach dem zweiten und dem dritten Element)
    # Die Elemente liegen alle auf der rechten Halbebene
    lst_roid_r = sorted(lst_roid_r, key=lambda x: (x[1], x[2]), reverse=False)
    lst_slop_r = list(sorted(lst_slop_r, reverse=False))
    # Sortiere die Liste absteigend (lst_roid nach dem zweiten und dem dritten Element)
    # Die Elemente liegen alle auf der linken Halbebene
    lst_roid_l = sorted(lst_roid_l, key=lambda x: (x[1], x[2]), reverse=True)
    lst_slop_l = list(sorted(lst_slop_l, reverse=True))

    # Kombiniere die Listen
    lst_roid = lst_roid_r + lst_roid_l
    lst_slop = lst_slop_r + lst_slop_l

    # Element mit der kleinsten Entfernung
    # (Achtung: in rechter HE sind alle Entfernungen negativ)
    # print(min(lst_roid, key=lambda t: t[2]))

    # Liste der Elemente mit Steigung 'inf'
    # print([num for num in lst_roid if num[1] == 12.0])
    # print(lst_roid)
    # Solange die Liste der Asteroiden nicht leer ist
    # laufe die verschiedenen Steigungen ab
    # nimm den Asteroiden mit der aktuellen Steigung und der kleinsten Distanz.
    # Achtung: Berücksichtige die Halbebene --> wenn Distanzen <= 0, dann sind sie rechts, sonst links.
    # Füge entferne ihn aus der Liste der Asteroiden und füge ihn der Liste der zerstörten hinzu
    #
    zaehler = 1
    ebene_r = True
    while lst_roid:
        for slop in lst_slop:
            if slop == float("-Inf"):
                ebene_r = True
            elif slop == float("Inf"):
                ebene_r = False

            if ebene_r:
                menge = [num for num in lst_roid if num[1] == slop and num[3]]
            else:
                menge = [num for num in lst_roid if num[1] == slop and not num[3]]
            if menge:
                a = min(menge, key= lambda t: t[2]) if ebene_r else max(menge)
                lst_roid.remove(a)
                if zaehler in [1, 2, 3, 10, 20, 50, 100, 199, 200, 201, 299]:
                    print(f"Nr. {zaehler} zerstört: {a}")
                zaehler += 1


# *norm2*   Euklidischer Abstand mittels Euklidischer Norm zwischen zwei Punkten v und w
def norm2(v, w=(14, 17)):
    abstand = math.sqrt((v[0] - w[0]) ** 2 + (v[1] - w[1]) ** 2)
    return abstand


# *slope*   Berechnet die "Steigung" m zwischen den Punkten v und w
#           Berechnet auch, in welchem Quadranten q sich der Punkt befindet
#           Steigungen in den Quadraten 2 und 3 sind positiv, in 1 und 4 negativ
def slope(v, w=(14, 17)):
    a = v[1] - w[1]  # Zähler
    b = v[0] - w[0]  # Nenner
    if a < 0 <= b:
        q = 1
    elif a >= 0 and b > 0:
        q = 2
    elif a > 0 and b <= 0:
        q = 3
    else:
        q = 4
    try:
        m = a / b
    except ZeroDivisionError:
        m = float("-Inf")  # if a >= 0 else float("-Inf")
    return m if q in [1, 2] else -m, q


# teil_2((11, 13))
teil_2()  # Lösung: 608


def slope_test():
    print("(12,7):", slope((12, 7), (11, 13)))
    print("(11, 7):", slope((11, 7), (11, 13)))
    print("(12,13)", slope((12, 13), (11, 13)))
    print("(12, 19):", slope((12, 19), (11, 13)))
    print("(11, 19):", slope((11, 19), (11, 13)))
    print("(10, 19):", slope((10, 19), (11, 13)))
    print("(10, 13):", slope((10, 13), (11, 13)))
    print("(10, 7):", slope((10, 7), (11, 13)))

# slope_test()

