# Advent of Code - Day 7
# Teil 1
import csv
import itertools  # itertools enthält eine Routine, die Permutationen erstellt
from intcode_computer_v2 import run_prog


with open('d:/42_python/aoc_data/day_9.csv') as f:
    aoc_input = [list(map(int, rec)) for rec in csv.reader(f, delimiter=',')][0]


def teil_1():
    print(run_prog(aoc_input.copy(), [1], startindex=0, debug=False, base=0))


# teil_1()  # 3_507_134_798


