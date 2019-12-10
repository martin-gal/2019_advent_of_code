# Advent of Code - Day 5
# Teil 1
import csv
import itertools  # itertools enthält eine Routine, die Permutationen erstellt
from intcode_computer import run_prog


with open('d:/42_python/aoc_data/day_7_test_4.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]

def teil_1():
    # Es gibt nun zwei Inputs
    # Der erste Input ist das phase setting \in {0, ..., 4}
    # Der zweite Input ist der Parameter (Startwert 0, sonst die Outputs der verschiedenen Instanzen)
    # Es gibt 5 Amps (A, B, C, D, E), jeder läuft auf einem eigenen Programm
    parameter = [0, 1, 2, 3, 4]
    phase_settings = list(itertools.permutations(parameter))
    thrust_sig = []
    # for startwert in phase_settings:
    #    print(run_prog(aoc_input.copy(), [startwert[0], 0]))

    # Die Ausgabe von Amp A ist der Input von Amp B, ..., die finale Ausgabe kommt von Amp E.
    for startwert in phase_settings:
        prog, output, halt = run_prog(aoc_input.copy(), [startwert[0], 0])                    # Amp A
        prog, output, halt = run_prog(aoc_input.copy(), [startwert[1], output])               # Amp B
        prog, output, halt = run_prog(aoc_input.copy(), [startwert[2], output])               # Amp C
        prog, output, halt = run_prog(aoc_input.copy(), [startwert[3], output])               # Amp D
        prog, output, halt = run_prog(aoc_input.copy(), [startwert[4], output])               # Amp E
        thrust_sig.append(output)

    lsg = max(thrust_sig)

    print(f"Das Maximum *{lsg}* wird durch die Konfiguration {phase_settings[thrust_sig.index(lsg)]} erreicht.")


# Teil 2
def teil_2():
    parameter = [5, 6, 7, 8, 9]
    phase_settings = list(itertools.permutations(parameter))

    thrust_sig = []

    for para in phase_settings:
        # Startzustände initialisieren
        prog_a = aoc_input.copy()
        prog_b = aoc_input.copy()
        prog_c = aoc_input.copy()
        prog_d = aoc_input.copy()
        prog_e = aoc_input.copy()
        startwert = 0
        while True:
            prog_a, output_a, halt_a = run_prog(prog_a, [para[0], startwert])
            prog_b, output_b, halt_b = run_prog(prog_b, [para[1], output_a])
            prog_c, output_c, halt_c = run_prog(prog_c, [para[2], output_b])
            prog_d, output_d, halt_d = run_prog(prog_d, [para[3], output_c])
            prog_e, startwert, halt_e = run_prog(prog_e, [para[4], output_d])
            if halt_e:
                thrust_sig.append(startwert)
                break

    print(thrust_sig)
    # Lösung: 4_248_984


teil_2()

