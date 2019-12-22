# Advent of Code - Day 13
"""
The arcade cabinet runs Intcode software like the game the Elves sent (your puzzle input). It has a primitive screen
capable of drawing square tiles on a grid. The software draws tiles to the screen with output instructions: every three
output instructions specify the x position (distance from the left), y position (distance from the top), and tile id.
The tile id is interpreted as follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a horizontal paddle tile (1 tile from the left and
2 tiles from the top) and a ball tile (6 tiles from the left and 5 tiles from the top).
"""
import csv
from intcode_computer_v3 import IntCodeComputer

with open('d:/42_python/2019_aoc/aoc_data/day_13.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]

# Teil 1: Start the game. How many block tiles are on the screen when the game exits?

# print(aoc_input)


def run_code():
    instanz_1 = IntCodeComputer(aoc_input.copy(), [0])
    while True:
        instanz_1.run_opcode()
        if instanz_1.halt:
            ausgabe = instanz_1.read_output()
            break
    return ausgabe


def count_tiles(nr):
    ausgabe = run_code()
    count = 0
    for i in range(2, len(ausgabe) + 1, 3):
        if ausgabe[i] == nr:
            count += 1
    return count


print(count_tiles(2))

# Teil 2:

board = dict()


def start_game(debug=False):
    instanz_1 = IntCodeComputer(aoc_input.copy(), [])
    instanz_1.set_value(0, 2)
    ball_x = paddle_x = None
    ball_y = paddle_y = None
    while not instanz_1.halt:
        x = y = tile = None
        instanz_1.run_opcode()
        if instanz_1.ausgabe and len(instanz_1.ausgabe) % 3 == 0:
            x = instanz_1.ausgabe.pop(0)        # x-Koordinate
            y = instanz_1.ausgabe.pop(0)        # y-Koordinate
            tile = instanz_1.ausgabe.pop(0)     # Feldart
            if x == -1:
                punkte = tile
                print_board(board)
                print(f"Aktueller Punktestand: {punkte}")
            else:
                paddle_x = x if tile == 3 else paddle_x
                paddle_y = y if tile == 3 else paddle_y
                if debug and paddle_x and ball_x and tile in [3, 4]:
                    print("Paddle: ", (paddle_x, paddle_y), "Ball: ", (ball_x, ball_y))
                if tile == 4:
                    # if ball_x and ball_y:
                    #     try:
                    #         schnitt_x, schnitt_y = ball_movement(ball_x, ball_y, x, y)
                    #     except TypeError:
                    #         None
                    ball_x = x
                    ball_y = y
                    if paddle_x:
                        move = (ball_x > paddle_x) - (ball_x < paddle_x)
                        print(f"Bewege um {move}") if debug else None
                        instanz_1.write_input(move)
                    else:
                        instanz_1.write_input(0)
                board[(x, y)] = tile
    ausgabe = instanz_1.read_output()
    return ausgabe


def print_board(brett):
    max_x = max(brett, key=lambda t: t[0])[0]
    max_y = max(brett, key=lambda t: t[1])[1]
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if brett[(x, y)] == 0:      # leeres Feld
                print(" ", end='')
            elif brett[(x, y)] == 1:    # Wand
                print("▒", end='')
            elif brett[(x, y)] == 2:    # zerstörbarer Block
                print("▄", end='')
            elif brett[(x, y)] == 3:    # steuerbares Panel
                print("─", end='')
            else:
                print("o", end='')      # Ball
        print('')


# Funktion, die den Schnittpunkt des Balls mit der Linie 20 berechnet und vollkommen nutzlos ist
def ball_movement(x_0, y_0, x_1, y_1):
    # bewegt der Ball sich nach oben oder unten?
    nach_unten = True
    if y_1 > y_0:
        nach_unten = True
    schrittweite = x_0 - x_1
    # abstand zur 20er Linie:
    abstand = 20 - y_1
    if nach_unten:
        if 0 < x_1 - abstand * schrittweite < 36:  # bounct der Ball von der Wand ab?
            print('Der Ball wird ', (x_1 - abstand * schrittweite, y_1 + abstand), 'kreuzen.')
            return x_1 - + abstand * schrittweite, y_1 + abstand  # den Punkt muss Paddle besetzen
        if x_1 - abstand * schrittweite < 0:    # + 3 ist nicht sicher
            print('Der Ball wird ', (abs(x_1 - abstand * schrittweite) + 3, y_1 + abstand), 'kreuzen.')
            return abs(x_1 - abstand * schrittweite) + 3, y_1 + abstand
        if 36 < x_1 - abstand * schrittweite:
            print('Der Ball wird ', (70 - (x_1 - abstand * schrittweite), y_1 + abstand), 'kreuzen.')
            return 70 - (x_1 - abstand * schrittweite), y_1 + abstand
    else:
        return None


print(start_game())

# print(ball_movement(16, 17, 17, 18))
# print(ball_movement(2, 10, 1, 11))
# print(ball_movement(33, 16, 34, 17))
# ******************************************************************************************************************** #
