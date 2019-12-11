# Advent of Code - Day 7
# Teil 1
import csv
import itertools  # itertools enthält eine Routine, die Permutationen erstellt
from intcode_computer import run_prog


with open('d:/42_python/aoc_data/day_7.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


def teil_1():
    # Es gibt nun zwei Inputs
    # Der erste Input ist das phase setting \in {0, ..., 4}
    # Der zweite Input ist der Parameter (Startwert 0, sonst die Outputs der verschiedenen Instanzen)
    # Es gibt 5 Amps (A, B, C, D, E), jeder läuft auf einem eigenen Programm
    parameter = [0, 1, 2, 3, 4]
    phase_settings = list(itertools.permutations(parameter))
    thrust_sig = []

    # Die Ausgabe von Amp A ist der Input von Amp B, ..., die finale Ausgabe kommt von Amp E.
    for startwert in phase_settings:
        prog, i, output, halt = run_prog(aoc_input.copy(), [startwert[0], 0])                    # Amp A
        prog, i, output, halt = run_prog(aoc_input.copy(), [startwert[1], output])               # Amp B
        prog, i, output, halt = run_prog(aoc_input.copy(), [startwert[2], output])               # Amp C
        prog, i, output, halt = run_prog(aoc_input.copy(), [startwert[3], output])               # Amp D
        prog, i, output, halt = run_prog(aoc_input.copy(), [startwert[4], output])               # Amp E
        thrust_sig.append(output)

    lsg = max(thrust_sig)

    print(f"Das Maximum *{lsg}* wird durch die Konfiguration {phase_settings[thrust_sig.index(lsg)]} erreicht.")


# Teil 2: Lösung: 4_248_984
# Die Amps gehen nun in einen Schleife, bis das Programm anhält. In dem Fall wird der letzte Output ausgeben.
def teil_2():
    parameter = [5, 6, 7, 8, 9]
    phase_settings = list(itertools.permutations(parameter))

    thrust_sig = []

    for para in phase_settings:
        par_set, output = teil_2_amp_connector(para)
        thrust_sig.append(output)
    lsg = max(thrust_sig)
    print(f"Das Maximum *{lsg}* wird durch die Konfiguration {phase_settings[thrust_sig.index(lsg)]} erreicht.")


# Die Funktion verknüpft die Amps und übergibt die Ausgabe des Amps als neuen Startparameter an den nächsten.
# Achtung: nach dem Start der Amps (mit den Phase Settings), werden nur noch die Ausgaben verarbeitet, nicht mehr
# die Phase Settings.
def teil_2_amp_connector(para=[6, 5, 9, 8, 7]):
    thrust_sig = []
    prog_a = aoc_input.copy()
    prog_b = aoc_input.copy()
    prog_c = aoc_input.copy()
    prog_d = aoc_input.copy()
    prog_e = aoc_input.copy()
    startwert = 0
    zaehler = 1
    i_a, i_b, i_c, i_d, i_e = 0, 0, 0, 0, 0
    # Erster Durchlauf:
    #   der erste Parameter ist phase_setting
    #   der zweite Parameter sind die Startwerte
    prog_a, i_a, output_a, halt_a = run_prog(prog_a, [para[0], startwert], i_a)
    prog_b, i_b, output_b, halt_b = run_prog(prog_b, [para[1], output_a], i_b)
    prog_c, i_c, output_c, halt_c = run_prog(prog_c, [para[2], output_b], i_c)
    prog_d, i_d, output_d, halt_d = run_prog(prog_d, [para[3], output_c], i_d)
    prog_e, i_e, startwert, halt_e = run_prog(prog_e, [para[4], output_d], i_e)
    while True:
        prog_a, i_a, output_a, halt_a = run_prog(prog_a, [startwert, 0], i_a)
        prog_b, i_b, output_b, halt_b = run_prog(prog_b, [output_a, 0], i_b)
        prog_c, i_c, output_c, halt_c = run_prog(prog_c, [output_b, 0], i_c)
        prog_d, i_d, output_d, halt_d = run_prog(prog_d, [output_c, 0], i_d)
        prog_e, i_e, startwert, halt_e = run_prog(prog_e, [output_d, 0], i_e)
        if startwert:
            thrust_sig.append(startwert)
        if halt_e:
            break
    return para, max(thrust_sig)


teil_1()
teil_2()

