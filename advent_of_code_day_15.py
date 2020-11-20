import csv
from intcode_computer_v3 import IntCodeComputer

with open('d:/42_python/2019_aoc/aoc_data/day_15.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


"""
The remote control program executes the following steps in a loop forever:

    Accept a movement command via an input instruction.
    Send the movement command to the repair droid.
    Wait for the repair droid to finish the movement operation.
    Report on the status of the repair droid via an output instruction.

Only four movement commands are understood: north (1), south (2), west (3), and east (4). Any other command is invalid. 
The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like 
4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

    0: The repair droid hit a wall. Its position has not changed.
    1: The repair droid has moved one step in the requested direction.
    2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen 
    system.

You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.

What is the fewest number of movement commands required to move the repair droid from its starting position to the 
location of the oxygen system?
"""

# TODO      Karte aufbauen:
#           gespeichert wird, ob ein Feld schon einmal besucht wurde
#           der Abstand zum Ursprung
#           das Oxygen System
# TODO      Algorithmus
#           leerer Raum: drehe Dich nach rechts und gehe vorwärts
#           Wand:        drehe Dich nach links und gehe vorwärts


board = dict()
board[(0, 0)] = dict()
board[(0, 0)]['visited'] = True
board[(0, 0)]['distance'] = 0
board[(0, 0)]['oxysys'] = False


class WallE:
    # Constructor
    def __init__(self, brett):
        self.pos = (0, 0)
        self.pos_alt = None
        self.direc_alt = None
        self.brett = brett

    def dfs(self, knoten):
        """ Tiefensuche mit Aktualisierung der Entfernung"""
        stack = [knoten]
        self.brett[knoten]['visited'] = True
        self.update_distance(knoten) if self.pos_alt is not None else None

    def move(self, direction):
        """ Gibt eine Richtung an (1 = Norden, 2 = Süden, 3 = Westen, 4 = Osten) und bewege den Roboter """
        a = self.pos
        self.direc_alt = direction
        self.pos_alt = a
        # TODO      Ändere die Position erst, wenn der Roboter zurück gegeben hat, dass es funktioniert hat
        # TODO      Füge das neue Feld dann dem Board hinzu (initialisiere mit dist "inf")
        if direction == 1:
            self.pos = (a[0], a[1] + 1)
        elif direction == 2:
            self.pos = (a[0], a[1] - 1)
        elif direction == 3:
            self.pos = (a[0] - 1, a[1])
        elif direction == 4:
            self.pos = (a[0] + 1, a[1])
        else:
            print(f"Ungültige Richtungsangabe {direction}")

    def update_distance(self, knoten):
        # nimm die distance des vorherigen Punktes, addiere eins drauf
        # ist diese dist < aktuelle Distanz des betrachteten Punktes, dann aktualisiere die dist
        a = self.brett[self.pos_alt]['distance']
        if a + 1 < self.brett[knoten]['distance']:
            self.brett[knoten]['distance'] = a + 1
            return True
        return False


def run_code():
    instanz_1 = IntCodeComputer(aoc_input.copy(), [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1])
    while True:
        instanz_1.run_opcode()
        print(instanz_1.read_output())
        if instanz_1.halt:
            ausgabe = instanz_1.read_output()
            break
    return ausgabe


print(run_code())

# -------------------------------------------------------------------------------------------------------------------- #
