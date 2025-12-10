# CSE-30151-Exam2-EC

Question 4: cnf_converter.py < input.json

This program takes a CFG and converts it to Chomsky Normal Form. 
It first takes the input.json which holds a CFG in the structure "Left": ["Right"] with the left being nonterminals and right being lists of symbols forming each production. 

First the program removes unit productions by replacing them with the productions of the nonterminal on the right. It does this by:
- Looping through every production in the grammar and checking whtether the right is a single nonterminal.
- If yes, it finds all productions of that nonterminal and adds those directly instead.
- It repeats this process in a loop until no more unit productions remain.

Next, it replaces terminals that appear inside longer productions. It does this by:
- Scanning every production with length >= 2
- If any of those sybmols is a terminanl, it creates a new variable
- It then replaces the terminal in the longer rule with its new variable
- A dictionary tracks which terminals already have replacements so no duplicates

Finally, the program breaks long productions into binary by:
- Looking for any rule with > 2 symbols on the right
- Starting from the left, it creates a series of new variables, each combining two symbols at once

This successfully transforms a CFG to Chomsky Normal Form.

Run: python3 cnf_converter.py < input.json
Output: {
  "S": [
    [
      "A",
      "B"
    ],
    [
      "X1",
      "X3"
    ],
    [
      "c"
    ],
    [
      "d"
    ],
    [
      "X2",
      "X4"
    ],
    [
      "X1",
      "X2"
    ],
    [
      "a"
    ]
  ],
  "A": [
    [
      "c"
    ],
    [
      "d"
    ],
    [
      "X2",
      "X4"
    ],
    [
      "X1",
      "X2"
    ],
    [
      "a"
    ]
  ],
  "B": [
    [
      "c"
    ],
    [
      "d"
    ],
    [
      "X2",
      "X4"
    ]
  ],
  "C": [
    [
      "c"
    ],
    [
      "d"
    ]
  ],
  "X1": [
    [
      "a"
    ]
  ],
  "X2": [
    [
      "b"
    ]
  ],
  "X3": [
    [
      "c"
    ]
  ],
  "X4": [
    [
      "d"
    ]
  ],
  "X5": [
    [
      "X1",
      "X2"
    ]
  ],
  "X6": [
    [
      "X2",
      "X3"
    ]
  ],
  "X7": [
    [
      "X2",
      "X3"
    ]
  ],
  "X8": [
    [
      "X2",
      "X3"
    ]
  ]
}

Question 5: cfg_operations.py < cfg2.json

This program takes two CFGs as json files and performs three operations: union, concatenation and kleene star. I then also hardcoded a test that builds a CFG for the Regex 0 U 10(000)* with our three operations.

First, the program loads both CFGs and renames the second grammar to avoid variable collisions.

Second, the program performs the union of the two CFGs by:
- Copying both grammars into one combined grammar
- Creating a brand new start symbol
- Adding productions from this symbol to the original start symbols

Next, it does the concatenations by:
- Combining grammars into one
- Creating a new start symbol
- Adding a production from the new start symbol to the start of the two grammars in order

Then, it performs the kleene star by:
- Copying the grammar
- Creating a new start symbol
- Adding the productions S -> e and S -> SS

Finally, the program runs the hardcoded example by:
- Creating small grammars for 0 and 1
- Concatenating them to form 10
- Concatenating three 0 grammars to form 000
- Applying Kleene star to get (000)*
- Concatenating to make 10(000)*
- Then taking the union with 0 to produce the full regex CFG

Run: python3 cfg_operations.py cfg1.json cfg2.json
Output:  
UNION(G1, G2)
{
  "S": [
    [
      "a",
      "S"
    ],
    [
      "a"
    ]
  ],
  "S1": [
    [
      "b",
      "S1"
    ],
    [
      "b"
    ]
  ],
  "S2": [
    [
      "S"
    ],
    [
      "S1"
    ]
  ]
}
Start symbol: S2 

CONCAT(G1, G2)
{
  "S": [
    [
      "a",
      "S"
    ],
    [
      "a"
    ]
  ],
  "S1": [
    [
      "b",
      "S1"
    ],
    [
      "b"
    ]
  ],
  "S2": [
    [
      "S",
      "S1"
    ]
  ]
}
Start symbol: S2 

STAR(G1)
{
  "S": [
    [
      "a",
      "S"
    ],
    [
      "a"
    ]
  ],
  "S1": [
    [
      "\u03b5"
    ],
    [
      "S",
      "S1"
    ]
  ]
}
Start symbol: S1 

Test CFG FOR 0 ∪ 10(000)*
{
  "T0": [
    [
      "0"
    ]
  ],
  "T1": [
    [
      "1"
    ]
  ],
  "T01": [
    [
      "0"
    ]
  ],
  "S1": [
    [
      "T1",
      "T01"
    ]
  ],
  "T011": [
    [
      "0"
    ]
  ],
  "T0111": [
    [
      "0"
    ]
  ],
  "S11": [
    [
      "T011",
      "T0111"
    ]
  ],
  "T02": [
    [
      "0"
    ]
  ],
  "S2": [
    [
      "S11",
      "T02"
    ]
  ],
  "S3": [
    [
      "\u03b5"
    ],
    [
      "S2",
      "S3"
    ]
  ],
  "S4": [
    [
      "S1",
      "S3"
    ]
  ],
  "S5": [
    [
      "T0"
    ],
    [
      "S4"
    ]
  ]
}
Start symbol: S5

Used ChatGPT with prompt "Help me understand the structure of this program and how I should approach the problem"

