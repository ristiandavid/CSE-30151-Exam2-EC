import json
import sys

def start(base, used):
    i = 1
    while f"{base}{i}" in used:
        i += 1
    return f"{base}{i}"

def load_cfg(path):
    with open(path) as f:
        g = json.load(f)
    start = list(g.keys())[0]
    return g, start

def copy_grammar(g):
    newg = {}
    for nt in g:
        rules = []
        for r in g[nt]:
            nr = []
            for s in r:
                nr.append(s)
            rules.append(nr)
        newg[nt] = rules
    return newg

def rename(g, start_sym, used):
    mapping = {}
    for nt in g:
        if nt in used:
            new = start(nt, used)
            mapping[nt] = new
            used.add(new)
        else:
            mapping[nt] = nt
            used.add(nt)

    newg = {}
    for old, new in mapping.items():
        rules = []
        for r in g[old]:
            nr = []
            for s in r:
                if s.isupper() and s in mapping:
                    nr.append(mapping[s])
                else:
                    nr.append(s)
            rules.append(nr)
        newg[new] = rules

    return newg, mapping[start_sym]

def cfg_union(G1, S1, G2, S2):
    used = set(G1.keys())
    for rules in G1.values():
        for r in rules:
            for s in r:
                if s.isupper():
                    used.add(s)

    G2r, S2r = rename(G2, S2, used)

    G = copy_grammar(G1)
    for nt in G2r:
        G[nt] = G2r[nt]

    newS = start("S", set(G.keys()))
    G[newS] = [[S1], [S2r]]

    return G, newS


def cfg_concat(G1, S1, G2, S2):
    used = set(G1.keys())
    for rules in G1.values():
        for r in rules:
            for s in r:
                if s.isupper():
                    used.add(s)

    G2r, S2r = rename(G2, S2, used)

    G = copy_grammar(G1)
    for nt in G2r:
        G[nt] = G2r[nt]

    newS = start("S", set(G.keys()))
    G[newS] = [[S1, S2r]]

    return G, newS


def cfg_star(G, S):
    G = copy_grammar(G)
    used = set(G.keys())
    newS = start("S", used)
    G[newS] = [["ε"], [S, newS]]
    return G, newS


def term(t):
    return {f"T{t}": [[t]]}, f"T{t}"


if len(sys.argv) == 3:
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    G1, S1 = load_cfg(file1)
    G2, S2 = load_cfg(file2)

    print("UNION(G1, G2)")
    U, Su = cfg_union(G1, S1, G2, S2)
    print(json.dumps(U, indent=2))
    print("Start symbol:", Su, "\n")

    print("CONCAT(G1, G2)")
    C, Sc = cfg_concat(G1, S1, G2, S2)
    print(json.dumps(C, indent=2))
    print("Start symbol:", Sc, "\n")

    print("STAR(G1)")
    K, Sk = cfg_star(G1, S1)
    print(json.dumps(K, indent=2))
    print("Start symbol:", Sk, "\n")

else:
    print("error")

# Build CFG for regex: 0 ∪ 10(000)*

G0, S0 = term("0")
G1t, S1t = term("1")

# 10
G10, S10 = cfg_concat(G1t, S1t, G0, S0)

# (000)
G000a, S000a = cfg_concat(G0, S0, G0, S0)
G000, S000 = cfg_concat(G000a, S000a, G0, S0)

# (000)*
Gstar, Sstar = cfg_star(G000, S000)

# 10(000)*
Gbig, Sbig = cfg_concat(G10, S10, Gstar, Sstar)

# 0 ∪ 10(000)*
Gfinal, Sfinal = cfg_union(G0, S0, Gbig, Sbig)

print("Test CFG FOR 0 ∪ 10(000)*")
print(json.dumps(Gfinal, indent=2))
print("Start symbol:", Sfinal)