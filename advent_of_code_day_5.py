# Advent of Code - Day 5
# Teil 1
import csv

with open('d:/42_python/aoc_data\day_5.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]

print(aoc_input)

# Es gibt mehrere opcodes der Form ABCDE
#   sind Zahlen nicht vorhanden, werden sie als 0 interpretiert
#   DE entspricht dem Opcode
#   A, B, C geben an, ob ein Parameter als Wert (1) oder als Verweis auf einen Parameter (0) interpretiert werden soll
#   Bsp: (00001, 2, 2, 3, 99)
#   01 -> addiere
#   0, 0, 0 --> Die Parameter sind als Positionen zu interpretieren
#   Nimm den Wert an Position 2 und addiere den mit dem Wert an Position 2 und schreibe das an Position 3
#   erzeugt: (00001, 2, 2, 4, 99)
#   Opcode 1 addiert (3 Parameter)
#   Opcode 2 multipliziert (3 Parameter)
#   Opcode 3 schreibt den Input (wird gesondert angegeben) an die Position seines Parameters (1 Parameter)
#   Opcode 4 gibt den Wert an der Position seines Parameters (1 Parameter) aus
#   Opcode 99 beendet das Programm
#
#   Es wird jetzt nicht mehr pauschal vier Schritte weitergegangen.

i = 0


# übergebe das Datenfeld, den Parameter-Schalter, und den Index und erhalte den Wert zurück
def zugriff(daten, handle, index):
    if handle == '0':
        return daten[daten[index]]
    else:
        return daten[index]


# Eingabe: Daten und Index des Opcodes
# Ausgabe: nächster Index und Daten
def f_opcode(daten, index, eingabe):
    ausgabe = 0
    wert = str(daten[index]).zfill(5)
    opcode = wert[3:]
    para_switch_c, para_switch_b, para_switch_a = wert[2], wert[1], wert[0]
    if opcode == '01':
        daten[daten[index + 3]] = zugriff(daten, para_switch_b, (index + 2)) \
                                  + zugriff(daten, para_switch_c, (index + 1))
        return daten, (index + 4), ausgabe
    elif opcode == '02':
        daten[daten[index + 3]] = zugriff(daten, para_switch_b, (index + 2)) \
                                  * zugriff(daten, para_switch_c, (index + 1))
        return daten, (index + 4), ausgabe
    elif opcode == '03':
        daten[daten[(index + 1)]] = eingabe
        return daten, (index + 2), ausgabe
    elif opcode == '04':
        ausgabe = zugriff(daten, para_switch_a, index + 1)
        return daten, (index + 2), ausgabe
    elif opcode == '99':
        return None
    else:
        print('Kein gültiger Opcode.')
        return None


# zaehler = 1
teil_1 = aoc_input.copy()
dc_input = 1
diagnose = []
while i < len(teil_1):
    iteration = f_opcode(teil_1, i, dc_input)
    if iteration is None:
        break
    teil_1 = iteration[0]
    i = iteration[1]
    diagnose.append(iteration[2])
    # print(f"{zaehler}:\t {teil_1} \t {i}")
    # zaehler += 1
print(diagnose[-1])

# Lösung 9654885


# Teil 2
#
#     Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value
#     from the second parameter. Otherwise, it does nothing.
#     Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from
#     the second parameter. Otherwise, it does nothing.
#     Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position
#     given by the third parameter. Otherwise, it stores 0.
#     Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
#     given by the third parameter. Otherwise, it stores 0.

teil_2 = aoc_input.copy()


def f_opcode_2(daten, index, eingabe):
    ausgabe = None
    wert = str(daten[index]).zfill(5)
    opcode = wert[3:]
    para_switch_c, para_switch_b, para_switch_a = wert[2], wert[1], wert[0]
    if opcode == '01':  # Addition
        daten[daten[index + 3]] = zugriff(daten, para_switch_b, (index + 2)) \
                                  + zugriff(daten, para_switch_c, (index + 1))
        return daten, (index + 4), ausgabe
    elif opcode == '02':  # Multiplikation
        daten[daten[index + 3]] = zugriff(daten, para_switch_b, (index + 2)) \
                                  * zugriff(daten, para_switch_c, (index + 1))
        return daten, (index + 4), ausgabe
    elif opcode == '03':  # Eingabe schreiben
        daten[daten[(index + 1)]] = eingabe
        return daten, (index + 2), ausgabe
    elif opcode == '04':  # Ausgabe schreiben
        ausgabe = zugriff(daten, para_switch_c, index + 1)
        print(f"Ausgabe: {ausgabe}")
        return daten, (index + 2), ausgabe
    elif opcode == '05':  # Springen wenn wahr
        if zugriff(daten, para_switch_c, index + 1) != 0:
            print(f"05: {zugriff(daten, para_switch_b, index + 2)}")
            return daten, zugriff(daten, para_switch_b, index + 2), ausgabe
        else:
            return daten, index + 3, ausgabe
    elif opcode == '06':  # Springen wenn falsch
        if zugriff(daten, para_switch_c, index + 1) == 0:
            print(f"06: {zugriff(daten, para_switch_b, index + 2)}")
            return daten, zugriff(daten, para_switch_b, index + 2), ausgabe
        else:
            return daten, index + 3, ausgabe
    elif opcode == '07':  # Kleiner als
        if zugriff(daten, para_switch_c, index + 1) < zugriff(daten, para_switch_b, index + 2):
            daten[daten[index + 3]] = 1
        else:
            daten[daten[index + 3]] = 0
        return daten, index + 4, ausgabe
    elif opcode == '08':  # Gleich
        if zugriff(daten, para_switch_c, index + 1) == zugriff(daten, para_switch_b, index + 2):
            daten[daten[index + 3]] = 1
        else:
            daten[daten[index + 3]] = 0
        return daten, index + 4, ausgabe
    elif opcode == '99':
        return None
    else:
        print('Kein gültiger Opcode.')
        return None


i = 0
print(f"0:\t {teil_2} \t {i}")
zaehler = 1
diag_input_2 = 5
diagnose_2 = []
while i < len(teil_2):
    iteration = f_opcode_2(teil_2, i, diag_input_2)
    if iteration is None:
        break
    teil_2 = iteration[0]
    i = iteration[1]
    if iteration[2] is not None:
        diagnose_2.append(iteration[2])
    print(f"{zaehler}:\t {teil_2} \t {i}")
    zaehler += 1
print(diagnose_2)  # Lösung 7079459
