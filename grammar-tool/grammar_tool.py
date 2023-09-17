'''
Parses and generates strings from a grammar.
'''

import sys
from source.generator import Generator
from source.grammar import Grammar
from tests.tests import Tests

try:
    MODE = sys.argv[1]

    if MODE not in ['generate', 'test']:
        raise ValueError('Invalid mode')

    DEPTH = int(sys.argv[2])

    if MODE == 'generate':
        FILENAME = sys.argv[3]
except (IndexError, ValueError) as error:
    print(error)
    print('Usage: python grammalyzer.py <mode> <depth> <filename>')
    sys.exit(1)

if MODE == 'generate':
    try:
        with open('samples/list_1.txt', 'r', encoding='utf-8') as file:
            grammar = Grammar(file.read())
    except (FileNotFoundError, KeyError, ValueError) as error:
        print(error)
        sys.exit(1)

    strings = Generator.generate_branches(grammar, DEPTH)

    for string in strings:
        print(string)
else:
    tests = Tests(DEPTH)
    tests.run_all()
