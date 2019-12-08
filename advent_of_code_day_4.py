# Advent of Code - Day 4
# Teil 1
# However, they do remember a few key facts about the password:
#
#     It is a six-digit number.
#     The value is within the range given in your puzzle input.
#     Two adjacent digits are the same (like 22 in 122345).
#     Going from left to right, the digits never decrease; they only ever
#     increase or stay the same (like 111123 or 135679).
#
# Gesucht: Anzahl der möglichen Passwörter im Schlüsselraum

prog_input = '124075-580769'
# prog_input = '123456-123466'

lower = int(prog_input[0:6])
upper = int(prog_input[-6:])
print(lower)
print(upper)
pwd_list = []

for pwd in range(lower, upper + 1):
    # print(pwd)
    check_pair = False
    check_dec = True
    for i in range(1, 6):
        # print(pwd % 10**(i+1) // 10**i, pwd % 10**i // 10**(i-1))
        if pwd % 10 ** (i + 1) // 10 ** i > pwd % 10 ** i // 10 ** (i - 1):
            check_dec = False
            break
        if pwd % 10 ** (i + 1) // 10 ** i == pwd % 10 ** i // 10 ** (i - 1):
            check_pair = True
    if check_dec and check_pair:
        pwd_list.append(pwd)

print(len(pwd_list))  # Lösung 2150

# Teil 2
# An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group
# of matching digits.
#
# Given this additional criterion, but still ignoring the range rule, the following are now true:
#
#     112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
#     123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
#     111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

pwd_list = []

for pwd in range(lower, upper + 1):
    # print(pwd)
    check_pair = False
    check_dec = True
    for i in range(1, 6):
        # print(pwd % 10**(i+1) // 10**i, pwd % 10**i // 10**(i-1))
        if pwd % 10 ** (i + 1) // 10 ** i > pwd % 10 ** i // 10 ** (i - 1):
            check_dec = False
            break
        if pwd % 10 ** (i + 1) // 10 ** i == pwd % 10 ** i // 10 ** (i - 1):
            if str((pwd % 10 ** (i + 1) // 10 ** i) * 111) not in str(pwd):
                check_pair = True
    if check_dec and check_pair:
        pwd_list.append(pwd)

print(len(pwd_list))  # Lösung: 1462