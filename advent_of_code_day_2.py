# Opcode 1 adds together numbers read from two positions and stores the result in a third position.
# The three integers immediately after the opcode tell you these three positions - the first two indicate the
# positions from which you should read the input values, and the third indicates the position at which the output
# should be stored.
#
# For example, if your Intcode computer encounters 1,10,20,30, it should read the values at positions 10 and 20,
# add those values, and then overwrite the value at position 30 with their sum.
#
# Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the
# three integers after the opcode indicate where the inputs and outputs are, not their values.
#
# Once you're done processing an opcode, move to the next one by stepping forward 4 positions.


# Daten importieren und als integer speichern
import csv
with open('d:/42_python/aoc_data\day_2_1.csv') as f:
    aoc_day_2 = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]

# Ausgabe des Inputs
print(aoc_day_2)

# Teil 1: Lösung 3516593

# initialisiere Zähler
i = 0

# Die Stelle 1 soll durch 12, die Stelle 2 durch 2 ersetzt werden
aoc_output_2 = aoc_day_2.copy()
aoc_output_2[1] = 12
aoc_output_2[2] = 2

# Laufe die Liste ab und verarbeite den Input
while i <= len(aoc_output_2) - 1:
    if aoc_output_2[i] == 1:
        aoc_output_2[aoc_output_2[i + 3]] = aoc_output_2[aoc_output_2[i + 1]] + aoc_output_2[aoc_output_2[i + 2]]
    elif aoc_output_2[i] == 2:
        aoc_output_2[aoc_output_2[i + 3]] = aoc_output_2[aoc_output_2[i + 1]] * aoc_output_2[aoc_output_2[i + 2]]
    elif aoc_output_2[i] == 99:
        break
    else:
        print('Fehler in der Verarbeitung: Kein Haltecode wurde getroffen.')
        break
    i += 4

print(aoc_output_2[0])

# Teil 2: Welcher Input (d.h. welche Zahlen an Stelle 1 und 2) erzeugt den Output 19690720? 7749
for k in range(100):
    for j in range(100):
        # print(f"Status: {aoc_output_2[1]}, {aoc_output_2[2]}")
        # Achtung: neue_liste = alte_liste erzeugt keine neue Liste sondern erzeugt nur eine Referenz. Änderungen an der
        # einen Liste wirken sich damit direkt auf die andere aus. Für eine Kopie ist alte_liste.copy() notwendig.
        aoc_output_2 = aoc_day_2.copy()
        # laenge = len(aoc_output_2)
        laenge, aoc_output_2[1], aoc_output_2[2] , i = len(aoc_output_2), k, j, 0
        # aoc_output_2[2] = j
        # i = 0
        # print(f"{aoc_output_2} \n{aoc_output_2[1]}\n{aoc_output_2[2]}\ni={i}\n{laenge}")
        # liste = []
        while i < laenge:
            # liste.append(aoc_output_2[i])
            # print(liste)
            if aoc_output_2[i] == 1:
                aoc_output_2[aoc_output_2[i + 3]] = aoc_output_2[aoc_output_2[i + 1]] + aoc_output_2[
                    aoc_output_2[i + 2]]
            elif aoc_output_2[i] == 2:
                aoc_output_2[aoc_output_2[i + 3]] = aoc_output_2[aoc_output_2[i + 1]] * aoc_output_2[
                    aoc_output_2[i + 2]]
            elif aoc_output_2[i] == 99:
                if aoc_output_2[0] == 19690720:
                    output = aoc_output_2[1] * 100 + aoc_output_2[2]
                    print(output)
                break
            else:
                print('Fehler in der Verarbeitung: Kein Haltecode wurde getroffen.')
                print(i, aoc_output_2[i])
                break
            i += 4