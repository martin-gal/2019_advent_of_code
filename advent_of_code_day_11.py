# Advent of Code - Day 11
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from intcode_computer_v3 import IntCodeComputer

with open('d:/42_python/2019_aoc/aoc_data/day_11.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


# TODO  get_color() schreiben --> Funktion, die die aktuelle Feldfarbe bekommt --> Input für den nächsten Durchlauf
# TODO  Ausgabe speichern: Zu Beginn ist das Feld komplett schwarz. Der Roboter gibt aus, ob er weiß oder schwarz
#       gemalt hat und wohin er sich als nächtes bewegt hat
# TODO  paint_tile(): weißt dem aktuellen Feld eine Farbe zu (abhängig vom Output[0]) und speichert, dass das Feld
#       bemalt wurde (boolean)
# TODO  Position des Roboters und Richtung in die er schaut
#       class Robot mit Richtung in U, D, L, R und Position und so
# TODO  move_robot() schreiben --> Bewegt den Roboter auf ein neues Feld
#       Wenn der Roboter aus dem Bereich rauslaufen würde, muss dieser wohl erweitert werden
# TODO  count_painted_tiles():
#       Zähler einbauen, wieviele Felder bemalt wurden. Allerdings zählt das nur bei Feldern, die noch nicht bemalt
#       wurden, d.h. auf dem Feld muss gespeichert werden, ob es schon einmal bemalt wurde
#       Achtung: Ein Feld wird erst bemalt, wenn es bemalt wurde. NICHT, wenn es besucht wird.


class Robot:

    def __init__(self, area, start=(0, 0)):
        self.blickrichtung = 'U'
        self.position = start
        self.tile_color = 0
        self.bereich = area

    def move_right(self):       # um 90° nach rechts drehen und einen Schritt gehen
        # print('move right')
        if self.blickrichtung == 'U':
            self.position = (self.position[0] + 1, self.position[1])
            self.blickrichtung = 'R'
        elif self.blickrichtung == 'R':
            self.position = (self.position[0], self.position[1] - 1)
            self.blickrichtung = 'D'
        elif self.blickrichtung == 'D':
            self.position = (self.position[0] - 1, self.position[1])
            self.blickrichtung = 'L'
        elif self.blickrichtung == 'L':
            self.position = (self.position[0], self.position[1] + 1)
            self.blickrichtung = 'U'

    def move_left(self):
        # print('move left')
        if self.blickrichtung == 'U':
            self.position = (self.position[0] - 1, self.position[1])
            self.blickrichtung = 'L'
        elif self.blickrichtung == 'L':
            self.position = (self.position[0], self.position[1] - 1)
            self.blickrichtung = 'D'
        elif self.blickrichtung == 'D':
            self.position = (self.position[0] + 1, self.position[1])
            self.blickrichtung = 'R'
        elif self.blickrichtung == 'R':
            self.position = (self.position[0], self.position[1] + 1)
            self.blickrichtung = 'U'

    def chk_tile(self):     # Prüft, ob das angesteuerte Feld noch im Bereich ist. Wenn nicht, wird dieser erweitert
        if self.position not in self.bereich:
            self.expand_area()
        # print('Check den Bereich.')

    def expand_area(self):
        # print('Bereich erweitert:', self.position)
        self.bereich[self.position] = dict()
        self.bereich[self.position]['farbe'] = 0
        self.bereich[self.position]['bemalt'] = False

    def get_color(self):
        self.tile_color = self.bereich[self.position]['farbe']
        return self.tile_color
        # print('Farbe des aktuellen Feldes:', self.tile_color)

    def move_robot(self, bewegung):
        self.move_left() if bewegung == 0 else self.move_right()
        self.chk_tile()

    def paint_tile(self, color):
        self.tile_color = color     # Farbe des aktuellen Feldes geändert
        self.bereich[self.position]['farbe'] = color
        self.bereich[self.position]['bemalt'] = True


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
    """ Zähle, wie viele Felder mindestens einmal bemalt werden """
    # Initialisiere den Bereich
    bereich = dict()
    bereich[(0, 0)] = dict()
    bereich[(0, 0)]['farbe'] = 0
    bereich[(0, 0)]['bemalt'] = False

    # count = 0
    # laenge = []
    sw_output = False                   # Prüft, ob es der erste (False) oder der zweite (True) Output ist
    # Erzeuge den Roboter
    wall_e = Robot(bereich)
    # instanz_1 ist die Steuereinheit des Roboters
    instanz_1 = IntCodeComputer(aoc_input.copy(), [0])
    while True:
        instanz_1.run_opcode()
        ausgabe = instanz_1.read_output()
        # laenge.append(len(ausgabe))
        if ausgabe:
            if not sw_output:           # Prüft, ob es der erste oder der zweite Output ist
                wall_e.paint_tile(ausgabe[-1])
                instanz_1.pop_output()
                sw_output = True
            else:
                # print(wall_e.position) if count == 100 else None
                wall_e.move_robot(ausgabe[-1])
                # print(wall_e.position) if count == 100 else None
                farbe = wall_e.get_color()
                # print(farbe) if count == 100 else None
                # print(bereich[wall_e.position]) if count == 100 else None
                instanz_1.write_input(farbe)
                instanz_1.pop_output()
                sw_output = False
        if instanz_1.halt:
            # print(laenge)
            return count_painted_tiles(bereich)
        # count += 1


def count_painted_tiles(felder):
    zaehler = 0
    for tile in felder:
        # zaehler += 1 if felder[tile]['bemalt'] else 0
        if felder[tile]['bemalt']:
            zaehler += 1
    return zaehler


# print(run_prog())       # Teil 1: Lösung 2255


# Teil 2: Male den Output, allerdings starte nun auf einem weißen Feld
def run_part_2():
    """ Mal den Output """
    # Initialisiere den Bereich
    bereich = dict()
    bereich[(0, 0)] = dict()
    bereich[(0, 0)]['farbe'] = 1            # Wir starten auf einem weißen Feld
    bereich[(0, 0)]['bemalt'] = False

    # count = 0
    # laenge = []
    sw_output = False                       # Prüft, ob es der erste (False) oder der zweite (True) Output ist
    # Erzeuge den Roboter
    wall_e = Robot(bereich)
    # instanz_1 ist die Steuereinheit des Roboters
    instanz_1 = IntCodeComputer(aoc_input.copy(), [wall_e.get_color()])
    while True:
        instanz_1.run_opcode()
        ausgabe = instanz_1.read_output()
        # laenge.append(len(ausgabe))
        if ausgabe:
            if not sw_output:               # Prüft, ob es der erste oder der zweite Output ist
                wall_e.paint_tile(ausgabe[-1])
                instanz_1.pop_output()
                sw_output = True
            else:
                # print(wall_e.position) if count == 100 else None
                wall_e.move_robot(ausgabe[-1])
                # print(wall_e.position) if count == 100 else None
                farbe = wall_e.get_color()
                # print(farbe) if count == 100 else None
                # print(bereich[wall_e.position]) if count == 100 else None
                instanz_1.write_input(farbe)
                instanz_1.pop_output()
                sw_output = False
        if instanz_1.halt:
            print_output(bereich)
            return count_painted_tiles(bereich)
        # count += 1


def print_output(liste):
    dpi = 80

    # Set red pixel value for RGB image
    red = [1, 0, 0]
    img = mpimg.imread("D:/42_python/ausgabe.png")
    height, width, bands = img.shape

    # Update red pixel value for RGBA image
    if bands == 4:
        red = [1, 0, 0, 1]

    # Update figure size based on image size
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    figure = plt.figure(figsize=figsize)
    axes = figure.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    axes.axis('off')

    faktor = 20

    for i in liste:
        if liste[i]['bemalt'] and liste[i]['farbe'] == 0:
            # img[-i[1]][i[0]] = red
            for j in range(-faktor*i[1],-faktor*i[1] + faktor):
                for k in range(faktor*i[0], faktor*i[0] + faktor):
                    img[j][k] = red

    # Draw the image
    axes.imshow(img)

    figure.savefig("test.png", dpi=dpi, transparent=True)


print(run_part_2())
# ******************************************************************************************************************** #
