# Advent of Code - Day 11
import csv
from intcode_computer_v3 import IntCodeComputer

with open('d:/42_python/2019_aoc/aoc_data/day_11.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


# Teil 1

# *run_prog* führt das Programm aus
# Input
#   programm        Das Programm, das bearbeitet werden soll
#   eingabe         Die Eingabe-Parameter
#   base            Die Basis, die im Modus 2 verwendet wird
#   startindex      Der Index, der verwendet werden soll
#   debug_mode      Gibt den aktuellen Durchlauf und den Status des Programms aus, wenn True
# Output
#   prog            Das modifizierte Programm
#   i               Der Index, an dem das Programm gestoppt hat
#   ausgabe         Der Ausgabewert des OpCode 04
#   halt            Der Zustand, ob das Programm angehalten hat oder nicht
def run_prog():
    instanz_1 = IntCodeComputer(aoc_input.copy(), [0])
    while True:
        instanz_1.run_opcode()
        if instanz_1.halt:
            print(instanz_1.prog)
            return instanz_1.read_output()
# TODO  Ausgabe als neue Eingabe schreiben - eingabe.append(a)
#       allerdings wird nur jede zweite Eingabe verwendet.
# TODO  get_color() schreiben --> Funktion, die die aktuelle Feldfarbe bekommt
# TODO  Ausgabe speichern: Zu Beginn ist das Feld komplett schwarz. Der Roboter gibt aus, ob er weiß oder schwarz
#       gemalt hat und wohin er sich als nächtes bewegt hat
# TODO  Zähler einbauen, wieviele Felder bemalt wurden. Allerdings zählt das nur bei Feldern, die noch nicht bemalt
#       wurden, d.h. auf dem Feld muss gespeichert werden, ob es schon einmal bemalt wurde
#       Achtung: Ein Feld wird erst bemalt, wenn es bemalt wurde. NICHT, wenn es besucht wird.

print(run_prog())
