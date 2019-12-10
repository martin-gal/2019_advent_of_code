# Advent of Code - Day 5
# Teil 1
import csv
import itertools  # itertools enthält eine Routine, die Permutationen erstellt

with open('d:/42_python/aoc_data/day_7.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


def zugriff(programm, handle, index):
    if handle == '0':
        return programm[programm[index]]
    else:
        return programm[index]


# Die Funktion verarbeitet den OpCode
# Als Rückgabewert gibt sie das (veränderte) Programm aus, den nächsten Index, der angesteuert werden soll,
# die Ausgabe, falls eine geschrieben wurde und den Index des nächsten Inputs
def run_opcode(programm, index, eingabe_index, eingabe):
    ausgabe = None
    wert = str(programm[index]).zfill(5)
    opcode = wert[3:]
    para_switch_c, para_switch_b, para_switch_a = wert[2], wert[1], wert[0]
    if opcode == '01':  # Addition
        programm[programm[index + 3]] = zugriff(programm, para_switch_b, (index + 2)) \
                                        + zugriff(programm, para_switch_c, (index + 1))
        return programm, (index + 4), ausgabe, eingabe_index, False
    elif opcode == '02':  # Multiplikation
        programm[programm[index + 3]] = zugriff(programm, para_switch_b, (index + 2)) \
                                        * zugriff(programm, para_switch_c, (index + 1))
        return programm, (index + 4), ausgabe, eingabe_index, False
    elif opcode == '03':  # Eingabe schreiben
        programm[programm[(index + 1)]] = eingabe[eingabe_index]
        return programm, (index + 2), ausgabe, eingabe_index + 1, False
    elif opcode == '04':  # Ausgabe schreiben
        ausgabe = zugriff(programm, para_switch_c, index + 1)
        # print(f"Ausgabe: {ausgabe}")
        return programm, (index + 2), ausgabe, eingabe_index, False
    elif opcode == '05':  # Springen wenn wahr
        if zugriff(programm, para_switch_c, index + 1) != 0:
            # print(f"05: {zugriff(programm, para_switch_b, index + 2)}")
            return programm, zugriff(programm, para_switch_b, index + 2), ausgabe, eingabe_index, False
        else:
            return programm, index + 3, ausgabe, eingabe_index, False
    elif opcode == '06':  # Springen wenn falsch
        if zugriff(programm, para_switch_c, index + 1) == 0:
            # print(f"06: {zugriff(programm, para_switch_b, index + 2)}")
            return programm, zugriff(programm, para_switch_b, index + 2), ausgabe, eingabe_index, False
        else:
            return programm, index + 3, ausgabe, eingabe_index, False
    elif opcode == '07':  # Kleiner als
        if zugriff(programm, para_switch_c, index + 1) < zugriff(programm, para_switch_b, index + 2):
            programm[programm[index + 3]] = 1
        else:
            programm[programm[index + 3]] = 0
        return programm, index + 4, ausgabe, eingabe_index, False
    elif opcode == '08':  # Gleich
        if zugriff(programm, para_switch_c, index + 1) == zugriff(programm, para_switch_b, index + 2):
            programm[programm[index + 3]] = 1
        else:
            programm[programm[index + 3]] = 0
        return programm, index + 4, ausgabe, eingabe_index, False
    elif opcode == '99':
        # return True
        return programm, index, ausgabe, eingabe_index, True
    else:
        print('Kein gültiger Opcode.')
        return None


# Es gibt nun zwei Inputs
# Der erste Input ist das phase setting \in {0, ..., 4}
# Der zweite Input ist der Parameter (Startwert 0, sonst die Outputs der verschiedenen Instanzen)
# Es gibt 5 Amps (A, B, C, D, E), jeder läuft auf einem eigenen Programm
parameter = [0, 1, 2, 3, 4]
phase_settings = list(itertools.permutations(parameter))


# Eingabe als Liste [phase_setting, input]
def run_prog(programm, eingabe):
    i = 0  # startindex des Programms
    eingabe_index = 0
    ausgabe = None
    zaehler = 1  # welcher Durchlauf/OpCode
    while i < len(programm):
        iteration = run_opcode(programm, i, eingabe_index, eingabe)
        # if iteration is None:
        #     break
        if iteration[4]:
            print('Angehalten')
            break
        programm = iteration[0]
        i = iteration[1]
        # if iteration[2] is not None:
        #     ausgabe.append(iteration[2])
        if iteration[2] is not None:
            ausgabe = iteration[2]
            return ausgabe
        eingabe_index = iteration[3]
        # print(f"{zaehler}:\t {programm} \t {i}")
        zaehler += 1
    return ausgabe, iteration[4]


thrust_sig = []
# for startwert in phase_settings:
#    print(run_prog(aoc_input.copy(), [startwert[0], 0]))

for startwert in phase_settings:
    output = run_prog(aoc_input.copy(), [startwert[0], 0])
    output = run_prog(aoc_input.copy(), [startwert[1], output])
    output = run_prog(aoc_input.copy(), [startwert[2], output])
    output = run_prog(aoc_input.copy(), [startwert[3], output])
    thrust_sig.append(run_prog(aoc_input.copy(), [startwert[4], output]))

lsg = max(thrust_sig)

print(f"Das Maximum *{lsg}* wird durch die Konfiguration {phase_settings[thrust_sig.index(lsg)]} erreicht.")

# Teil 2
parameter = [5, 6, 7, 8, 9]
phase_settings = list(itertools.permutations(parameter))

thrust_sig = []
prog_a = aoc_input.copy()
prog_b = aoc_input.copy()
prog_c = aoc_input.copy()
prog_d = aoc_input.copy()
prog_e = aoc_input.copy()

startwert = 0
for para in phase_settings:
    while True:
        output = run_prog(prog_a, [para[0], startwert])
        output = run_prog(prog_b, [para[1], output])
        output = run_prog(prog_c, [para[2], output])
        output = run_prog(prog_d, [para[3], output])
        startwert = run_prog(prog_e, [para[4], output])
        if not isinstance(startwert, int):
            thrust_sig.append(startwert[0])
            break

print(thrust_sig)
#
# Das run_prog muss vermutlich die Programme zurückgeben