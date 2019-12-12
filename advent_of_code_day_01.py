# Advent of Code - Day 1
# Teil 1
# Fuel required to launch a given module is based on its mass.
# Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2

# Daten importieren und als integer speichern
# import csv
with open('d:/42_python/2019_aoc/aoc_data/day_1_1.csv') as f:
    aoc_day_1 = [int(i) for i in f]

# Ausgabe des Inputs
print(aoc_day_1)

# Durch 3 teilen und abrunden entspricht div 3
#   Lösung 1 mit divmod-Funktion
# aoc_output_1 = list(map(lambda x: divmod(x,3), aoc_day_1))
# aoc_output_1 = [aoc_output_1[i][0] - 2 for i in range(0, len(aoc_output_1))]
#   Lösung 2 mit // Operator
# aoc_output_1 = [aoc_day_1[i] // 3 - 2 for i in range(0, len(aoc_day_1))]

# Lösung Teil 1: 3249140
print(sum([aoc_day_1[i] // 3 - 2 for i in range(len(aoc_day_1))]))

print(sum(i // 3 - 2 for i in aoc_day_1)) # etwas eleganter

# Teil 2
# Das Gewicht des Treibstoffs muss hinzuaddiert werden, so lange dieser positiv ist
# Lösung Teil 2: 4870838
fuel = 0
# Berechne für jedes Modul den Treibstoff-Bedarf, sowie den Treibstoff-Bedarf für den Treibstoff,
# solange dieser positiv ist
for i in range(len(aoc_day_1)):
    j = aoc_day_1[i]
    while j > 0:
        j = j // 3 - 2
        fuel = fuel + max(j, 0)

print(fuel)

# etwas eleganter
fuel = 0
for i in aoc_day_1:
    while i > 0:
        i = i // 3 - 2
        fuel += max(i, 0)

print(fuel)
