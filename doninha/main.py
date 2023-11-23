import string
from random import choice, randrange


def calculate_distance(string1, string2):
    return sum(c1 != c2 for c1, c2 in zip(string1, string2))


letters = string.ascii_uppercase + " "

target = "METHINKS IT IS LIKE A WEASEL"

initial_string = "".join(choice(letters) for _ in target)
assert len(initial_string) == len(target)
distance = calculate_distance(target, initial_string)
generation = 0
for n in range(10000):
    modif_caracter = randrange(len(initial_string))
    mutant = initial_string[:modif_caracter] + choice(letters) + initial_string[modif_caracter + 1:]

    mdist = calculate_distance(target, mutant)

    if mdist < distance:
        initial_string, distance = mutant, mdist
        generation += 1
        print("generation:", generation, "mutant number:", n, ":", initial_string)
        if distance == 0:
            break
