# Advent of Code - Day 14

import networkx as nx
import matplotlib.pyplot as plt

with open('d:/42_python/2019_aoc/aoc_data/day_14_test_1.txt') as f:
    aoc_input = f.read().splitlines()

# print(aoc_input)

"""
Teil 1 
As you approach the rings of Saturn, your ship's low fuel indicator turns on. There isn't any fuel here, but the rings 
have plenty of raw material. Perhaps your ship's Inter-Stellar Refinery Union brand nanofactory can turn these raw 
materials into fuel.

You ask the nanofactory to produce a list of the reactions it can perform that are relevant to this process 
(your puzzle input). Every reaction turns some quantities of specific input chemicals into some quantity of an output 
hemical. Almost every chemical is produced by exactly one reaction; the only exception, ORE, is the raw material input 
to the entire process and is not produced by a reaction.

You just need to know how much ORE you'll need to collect before you can produce one unit of FUEL.

Test 1      -        31
Test 1_2    -       165 
Test 2      -    13_312 
Test 3      -   180_697 
Test 4      - 2_210_736
"""
# [X]   Datenstruktur für den Input anlegen
#       Alles rechts von => ist das Ergebnis
# TODO  Rückwärtssuche implementieren
# TODO  Produktionsüberschuss beachten

zutaten = ['ORE']
rezept = dict()

G = nx.Graph()


def create_input():
    for ipt in aoc_input:
        eingabe, ergebnis = ipt.split(' => ')
        a = ergebnis.split()
        liste = {item[1]: int(item[0]) for item in [item.split() for item in eingabe.split(', ')]}
        rezept[a[1]] = {'menge': int(a[0]), 'zutaten': liste}
        zutaten.append(a[1])


create_input()
schritte = ['FUEL']
# print(schritte)
# print(rezept)
zaehler = 0

G.add_nodes_from(zutaten)

print(G)
# plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
# while len(schritte) < len(zutaten):
for item in zutaten:
    print(rezept[item]['zutaten'].keys())
    # break

# print(len(zutaten))
#
# for i in zutaten:
#     print(i)
#
#
# print(rezept)
#
# print(rezept['FUEL'])
# for i in rezept['FUEL']['zutaten']:
#     print(i)
#
# print(rezept.keys())


# ******************************************************************************************************************** #
