import string
from random import choice, randrange


def calculate_distance(string1, string2):
    return sum(c1 != c2 for c1, c2 in zip(string1, string2))


letters = string.ascii_letters + " "

target = "ME THINKS IT IS LIKE A WEASEL"

initial_string = "".join(choice(letters) for _ in target)
assert len(initial_string) == len(target)
dist = calculate_distance(target, initial_string)
generation = 0
for n in range(10000):
    place = randrange(len(initial_string))
    mutant = initial_string[:place] + choice(letters) + initial_string[place + 1:]

    assert len(initial_string) == len(mutant)

    mdist = calculate_distance(target, mutant)
    if mdist < dist:
        initial_string, dist = mutant, mdist
        generation += 1
        print(generation, n, ":", initial_string)
        if mutant == target:
            break
