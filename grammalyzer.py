'''
Parses and generates strings from a grammar.
'''

import sys
from source.generator import Generator
from source.grammar import Grammar

if len(sys.argv) < 3:
    print("Usage: python main.py <filename> <string_count>")
    sys.exit(1)

FILENAME = sys.argv[1]

try:
    STRING_COUNT = int(sys.argv[2])
except ValueError:
    print("Invalid string count.")
    sys.exit(1)

try:
    with open(FILENAME, 'r', encoding='utf-8') as file:
        grammar = Grammar(file.read())
except (FileNotFoundError, KeyError, ValueError) as error:
    print(error)
    sys.exit(1)

generator = Generator(grammar)
generator.run(STRING_COUNT)

for string in generator.strings:
    print(string)
