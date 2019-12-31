# Advent of Code - Day 16
import numpy as np
from timeit import Timer

with open('d:/42_python/2019_aoc/aoc_data/day_16.txt') as f:
    aoc_input = [int(dat) for dat in f.read().splitlines()[0]]

# print(aoc_input[0])
# eingabe = list(aoc_input[0])

"""
Each element in the new list is built by multiplying every value in the input list by a value in a repeating pattern and
then adding up the results. So, if the input list were 9, 8, 7, 6, 5 and the pattern for a given element were 1, 2, 3, 
the result would be 9*1 + 8*2 + 7*3 + 6*1 + 5*2 (with each input element on the left and each value in the repeating 
pattern on the right of each multiplication). Then, only the ones digit is kept: 38 becomes 8, -17 becomes 7, and so on.

While each element in the output array uses all of the same input array elements, the actual repeating pattern to use 
depends on which output element is being calculated. The base pattern is 0, 1, 0, -1. Then, repeat each value in the 
pattern a number of times equal to the position in the output list being considered. Repeat once for the first element,
twice for the second element, three times for the third element, and so on. So, if the third element of the output list
is being calculated, repeating the values would produce: 0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1.

When applying the pattern, skip the very first value exactly once. (In other words, offset the whole pattern left by 
one.) So, for the second element of the output list, the actual pattern used would be: 
0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1, ....

test_1          24176176
test_2          73745418
test_3          52432133
"""

base_pattern = ['0', '1', '0', 'a']


def fft(num_phase, daten, debug=False):
    liste = aoc_input.copy()
    phase = 1
    while phase <= num_phase:
        zaehler = 1
        temp_liste = liste.copy()
        while zaehler <= len(liste):
            c = 0
            """ base_pattern vorbereiten """
            pattern = []
            while len(pattern) <= len(liste):
                pattern += base_pattern[0] * zaehler
                pattern += base_pattern[1] * zaehler
                pattern += base_pattern[2] * zaehler
                pattern += base_pattern[3] * zaehler
            pattern = [string.replace('a', '-1') for string in pattern[1:len(liste)+1]]
            # print(pattern)
            for j in range(0, len(liste)):
                a = int(liste[j])
                # print(a)
                try:
                    b = int(pattern[j])
                except IndexError:
                    print(j)
                # print(b)
                c += a * b
            temp_liste[j] = abs(c) % 10
            zaehler += 1
        liste = temp_liste.copy()
        print(f"Phase {phase}, Liste: {liste}") if debug else None
        phase += 1
        print(phase)
    return liste


def fft2(num_phase, daten, debug=False):
    liste = np.array(aoc_input.copy())
    print(liste) if debug else None
    phase = 1
    while phase <= num_phase:
        zaehler = 1
        temp_liste = []
        while zaehler <= len(liste):
            c = 0
            """ base_pattern vorbereiten """
            pattern = []
            while len(pattern) <= len(liste):
                pattern += base_pattern[0] * zaehler
                pattern += base_pattern[1] * zaehler
                pattern += base_pattern[2] * zaehler
                pattern += base_pattern[3] * zaehler
            pattern = np.array([int(string.replace('a', '-1')) for string in pattern[1:len(liste)+1]])
            print(pattern) if debug else None
            c = abs(sum(pattern * liste)) % 10
            temp_liste.append(c)
            zaehler += 1
        liste = temp_liste.copy()
        print(f"Phase {phase}, Liste: {liste}") if debug else None
        phase += 1
        print(phase)
    return liste

# print(fft(100, aoc_input[0])[0:8])
# print(fft2(100, aoc_input[0])[0:8])


""" 
Teil 2

Die ersten 7 Stellen des Inputs geben den Offset an, d.h. den Punkt, ab dem die 8stellige Ausgabe beginnt.
Offset: 5_977_341
Der Input, der verarbeitet werden soll, ist der Original-Input nur 10_000 fach wiederholt, d. h. er hat eine Länge von
6_500_000 Stellen.
Da der Offset 5_977_341 beträgt und die Stellen davor für die Folgestellen nicht relevant sind (durch die 0en im Basic-
Pattern werden diese irrelevant), kann der Input drastisch reduziert werden.
Weiterhin gilt: 
    -   Da ab der Stelle Offset das Basic-Pattern jetzt mit 1en aufgefüllt wird, und Offset > 6_500_000 / 2, 
        werden die weiteren Einträge des Basic-Patterns (0, -1) irrelevant. Es folgen nur noch 1er Stellen im 
        Basic-Pattern.
    -   Man kann "rückwärts" rechnen: 
        a + b + c + d + e = f = a + g
            b + c + d + e = g = b + h
                c + d + e = h = c + i
                    d + e = i = d + j
                        e = j
"""

teil_2_input = aoc_input * 10000
offset = int(''.join(map(str, teil_2_input[:7])))
# print(offset)

# reduziere Input
teil_2_input = teil_2_input[offset:]
# berechne FFT
zaehler = 1
num_phase = 100
while zaehler <= num_phase:
    for i in range(len(teil_2_input)-1, 0, -1):
        try:
            teil_2_input[i-1] = (teil_2_input[i-1] + teil_2_input[i]) % 10
        except IndexError:
            print(f"Index: {i}")
    zaehler += 1
    # print(f"Phase: {zaehler}, Liste: {teil_2_input}")

print(teil_2_input[:8])
# for i in enumerate(aoc_input):
#     print(i)
# print(aoc_input)
# -------------------------------------------------------------------------------------------------------------------- #
