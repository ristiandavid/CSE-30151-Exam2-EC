import json
from collections import defaultdict

with open("input.json") as file_handle:
    grammar = json.load(file_handle)

counter = 1
def start():
    global counter
    new = f"X{counter}"
    counter += 1
    return new

def remove_units(grammar):
    changed = True
    while changed:
        changed = False
        new_grammar = defaultdict(list)
        for nt in grammar:
            for right in grammar[nt]:
                if len(right)==1 and right[0].isupper():
                    unt = right[0]
                    for prod in grammar[unt]:
                        if prod not in grammar[nt]:
                            new_grammar[nt].append(prod)
                            changed = True
                else:
                    new_grammar[nt].append(right)
        grammar = new_grammar
    return grammar

def replace_terminals(grammar):
    terminal_map = {}
    for nt in list(grammar.keys()):
        new_prod = []
        for right in grammar[nt]:
            if len(right) >= 2:
                new_right = []
                for symbol in right:
                    if symbol.islower():
                        if symbol not in terminal_map:
                            new_variable = start()
                            terminal_map[symbol] = new_variable
                            grammar[new_variable] = [[symbol]]
                        new_right.append(terminal_map[symbol])
                    else:
                        new_right.append(symbol)
                new_prod.append(new_right)
            else:
                new_prod.append(right)
        grammar[nt] = new_prod
    return grammar


def break_long(grammar):
    for nt in list(grammar.keys()):
        new_prod = []
        for right in grammar[nt]:
            if len(right) <= 2:
                new_prod.append(right)
            else:
                curr = right[0]
                for index in range(1, len(right)-1):
                    new_variable = start()
                    grammar[new_variable] = [[curr, right[index]]]
                    curr_variable = new_variable
                new_prod.append([curr, right[-1]])
        grammar[nt] = new_prod
    return grammar

grammar = remove_units(grammar)
grammar = replace_terminals(grammar)
grammar = break_long(grammar)

print(json.dumps(grammar, indent=2))

