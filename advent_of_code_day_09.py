# Advent of Code - Day 9
import csv
# import itertools  # itertools enthält eine Routine, die Permutationen erstellt
from intcode_computer_v2 import run_prog


with open('d:/42_python/2019_aoc/aoc_data/day_9.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


# Teil 1: Vervollständige den Intcode Computer
def teil_1():
    a = aoc_input.copy()
    print(run_prog(a, [1], startindex=0, debug=False, base=0))
    print(a)


teil_1()  # 3_507_134_798


# Teil 2: Eingabe = 2
def teil_2():
    print(run_prog(aoc_input.copy(), [2]))


teil_2()    # 84_513

