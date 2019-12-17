# Advent of Code - Day 12
import math

with open('d:/42_python/2019_aoc/aoc_data/day_12.txt') as f:
    aoc_input = [i for i in f]

# print(aoc_input)

# <x=-4, y=-9, z=-3>
# <x=-13, y=-11, z=0>
# <x=-17, y=-7, z=15>
# <x=-16, y=4, z=2>

# Initialisiere die Monde
moons = dict()
for i in range(1, 5):
    moons[i] = dict()
    moons[i]['vel'] = (0, 0, 0)

moons[1]['pos'] = (-4, -9, -3)
moons[2]['pos'] = (-13, -11, 0)
moons[3]['pos'] = (-17, -7, 15)
moons[4]['pos'] = (-16, 4, 2)

startwerte = dict()
for i in range(1, 5):
    startwerte[i] = dict()
    startwerte[i]['vel'] = (0, 0, 0)

startwerte[1]['pos'] = (-4, -9, -3)
startwerte[2]['pos'] = (-13, -11, 0)
startwerte[3]['pos'] = (-17, -7, 15)
startwerte[4]['pos'] = (-16, 4, 2)

# moons[1]['pos'] = (-1, 0, 2)
# moons[2]['pos'] = (2, -10, -7)
# moons[3]['pos'] = (4, -8, 8)
# moons[4]['pos'] = (3, 5, -1)


# Teil 1: Gesamtenergie des Systems nach 1_000 Schritten
def update_states():
    """ Aktualisiert zunächst die Geschwindigkeit und anschließend die Position der Monde"""
    for idx in range(1, 5):
        update_velocity(idx)
    for idx in range(1, 5):
        update_position(idx)


def update_velocity(idx):
    """ Aktualisiert die Geschwindigkeit von Mond idx
    TODO    Die Positionen bzw. die Geschwindigkeiten ändern sich zu stark
    """

    monde = moons.copy()
    betrachter = monde.pop(idx)
    a = moons[idx]['vel']
    for i in range(0, 3):
        counter = 0
        for mond in monde:
            # In der IF Bedingung ist irgendwo ein Fehler...
            # betrachter['pos'][i] ist korrekt
            if betrachter['pos'][i] < monde[mond]['pos'][i]:
                counter += 1
            elif betrachter['pos'][i] > monde[mond]['pos'][i]:
                counter += -1
            else:
                counter += 0
        if i == 0:
            a = (a[0] + counter, a[1], a[2])
        elif i == 1:
            a = (a[0], a[1] + counter, a[2])
        else:
            a = (a[0], a[1], a[2] + counter)

    moons[idx]['vel'] = a


def update_position(idx):
    """ Aktualisiert die Position des aktuellen Monds """
    moons[idx]['pos'] = tuple(pos + vel for pos, vel in zip(moons[idx]['pos'], moons[idx]['vel']))


def total_energy():
    """ Berechnet die Gesamtenergie des Systems """
    energy = 0
    for moon in moons:
        a = sum(tuple(map(abs, moons[moon]['pos'])))
        b = sum(tuple(map(abs, moons[moon]['vel'])))
        energy += a*b
    return energy


zaehler = 0
while zaehler < 1000:
    update_states()
    zaehler += 1


print("Gesamtenergie des Systems nach 1000 Schritten: ", total_energy())  # Teil 1: Lösung 6220


# Teil 2: Nach wievielen Schritten ist das System wieder am Anfang?
# Lösungsansatz:    x, y, z sind unabhängig voneinander.
#                   D.h. Berechne die Anzahl der Schritte, bis alles wieder so ist für x, y, z unabhängig.
# Die Lösung ist dann das kleinste gemeinsame Vielfache von den dreien.

def update_velocity_i(idx, i):
    """ Aktualisiert die Geschwindigkeit von Mond idx
    TODO    Die Positionen bzw. die Geschwindigkeiten ändern sich zu stark
    """

    monde = moons.copy()
    betrachter = monde.pop(idx)
    a = moons[idx]['vel']
    counter = 0
    for mond in monde:
        # In der IF Bedingung ist irgendwo ein Fehler...
        # betrachter['pos'][i] ist korrekt
        if betrachter['pos'][i] < monde[mond]['pos'][i]:
            counter += 1
        elif betrachter['pos'][i] > monde[mond]['pos'][i]:
            counter += -1
        else:
            counter += 0
    if i == 0:
        a = (a[0] + counter, a[1], a[2])
    elif i == 1:
        a = (a[0], a[1] + counter, a[2])
    else:
        a = (a[0], a[1], a[2] + counter)

    moons[idx]['vel'] = a


def update_states_i(i):
    """ Aktualisiert zunächst die Geschwindigkeit und anschließend die Position der Monde"""
    for idx in range(1, 5):
        update_velocity_i(idx, i)
    for idx in range(1, 5):
        update_position(idx)


# print(moons)
# print(startwerte[1]['pos'])
# update_states_i(0)
# print(startwerte[1]['pos'])
# print(moons[1]['pos'])
# print(moons)

count = [1, 1, 1]

# Nach jedem Durchlauf müssen die Monde auf die Startwerte gesetzt werden.
# Oder der Vorgang dreimal manuell wiederholt und die Zahlen eingesetzt...

for j in range(0, 3):
    moons = dict()
    for i in range(1, 5):
        moons[i] = dict()
        moons[i]['vel'] = (0, 0, 0)

    moons[1]['pos'] = (-4, -9, -3)
    moons[2]['pos'] = (-13, -11, 0)
    moons[3]['pos'] = (-17, -7, 15)
    moons[4]['pos'] = (-16, 4, 2)

    while True:
        update_states_i(j)
        count[j] += 1
        if startwerte[1]['pos'] == moons[1]['pos'] \
                and startwerte[2]['pos'] == moons[2]['pos'] \
                and startwerte[3]['pos'] == moons[3]['pos'] \
                and startwerte[4]['pos'] == moons[4]['pos']:
            break

print(count)


# kleinstes gemeinsames Vielfaches
def lcm(x_1, x_2):
    return abs(x_1 * x_2) // math.gcd(x_1, x_2)


# x-Koordinate: 231614 Durchläufe
# y-Koordinate: 167624 Durchläufe
# z-Koordinate: 113028 Durchläufe
kgv_1 = lcm(count[0], count[1])
kgv_2 = lcm(kgv_1, count[2])


print("Anzahl der Schritte bis zum Ursprung: ", kgv_2)  # Teil 2: Lösung 548525804273976

# ******************************************************************************************************************** #
