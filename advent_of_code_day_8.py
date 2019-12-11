# Advent of Code - Day 7
# Teil 1
# Ein Bild wird geschickt, welches zwei Layer besitzt
# Jeder Layer hat die Dimention 25 x 6

with open('d:/42_python/aoc_data/day_8.txt') as f:
    aoc_input = [i for i in f][0]


def teil_1(daten, dim_x=25, dim_y=6):
    # die Anzahl der Layer entspricht der Länge des Inputs div (dim_x * dim_y)
    anzahl_layer = (len(daten)) // (dim_x * dim_y)
    # print(f"Die Anzahl der Layer ist {anzahl_layer}.")
    bild_speicher = dict()
    checker = list()
    for i in range(1, anzahl_layer + 1):
        bild_speicher[i] = daten[(i - 1) * (dim_x * dim_y):(i * (dim_x * dim_y))]
        checker.append(chksum(bild_speicher[i]))
    print(min(checker, key=lambda t: t[0]))
    print(f"Der Layer {checker.index(min(checker, key=lambda t: t[0]))} besitzt am wenigsten 0en.")
    print(bild_speicher[1])


# chksum prüft, ob das Bild den Vorgaben entspricht
# Input
#   bild        Das Bild als Zeichenkette
# Output
#   anzahl_0    Die Anzahl der 0er des Layers
#   check       Die Anzahl der 1er multipliziert mit der Anzahl der 2er
def chksum(bild):
    anzahl_0 = bild.count('0')
    check = bild.count('1') * bild.count('2')
    return anzahl_0, check


# teil_1(aoc_input)  # Lösung 2016 (8 Nullen, Layer 5)


# Teil 2
# Die einzelnen Layer müssen nun übereinander gelegt werden, Layer 1 ist ganz vorne
# 0     schwarz
# 1     weiß
# 2     transparent
def teil_2(daten, dim_x=25, dim_y=6):
    # die Anzahl der Layer entspricht der Länge des Inputs div (dim_x * dim_y)
    anzahl_layer = (len(daten)) // (dim_x * dim_y)
    layer = dict()
    for i in range(1, anzahl_layer + 1):
        zeile = dict()
        for j in range(1, dim_y + 1):
            zeile[j] = daten[((dim_x * (j - 1)) + (dim_x * dim_y * (i - 1))):((dim_x * j) + (dim_x * dim_y * (i - 1)))]
        layer[i] = zeile

    bild = dict()
    for nr_zle in range(1, dim_y + 1):
        bild[nr_zle] = ''
        for nr_pix in range(1, dim_x + 1):
            for nr_lyr in range(1, anzahl_layer + 1):
                # print(nr_zle, nr_pix, nr_lyr)
                if int(layer[nr_lyr][nr_zle][(nr_pix-1):nr_pix]) == 1:
                    bild[nr_zle] = bild[nr_zle] + '#'
                    break
                elif int(layer[nr_lyr][nr_zle][(nr_pix-1):nr_pix]) == 0:
                    bild[nr_zle] = bild[nr_zle] + ' '
                    break
            # print(bild[nr_zle])
    for nr_zle in range(1, dim_y + 1):
        print(bild[nr_zle])


teil_2(aoc_input)  # Lösung: HZCZU
