'''
Parses and generates strings from a grammar.
'''

import sys
from source.generator import Generator
from source.grammar import Grammar

if len(sys.argv) < 3:
    print("Usage: python grammalyzer.py <filename> <depth>")
    sys.exit(1)

FILENAME = sys.argv[1]

try:
    DEPTH = int(sys.argv[2])
except ValueError:
    print("Invalid depth.")
    sys.exit(1)

try:
    with open('samples/list_1.txt', 'r', encoding='utf-8') as file:
        grammar = Grammar(file.read())
except (FileNotFoundError, KeyError, ValueError) as error:
    print(error)
    sys.exit(1)

strings = Generator.generate_branches(grammar, DEPTH)

for string in strings:
    print(string)
