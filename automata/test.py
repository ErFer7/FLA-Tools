'''
Test.
'''

from os.path import join
from json import loads
from tests.tests import Tests

with open(join('tests','cases', 'determinization.json'), 'r') as file:
    nfa_automata = loads(file.read())

with open(join('tests', 'cases', 'minimization.json'), 'r') as file:
    dfa_automata = loads(file.read())

nfa_tests = Tests(nfa_automata.items())
dfa_tests = Tests(dfa_automata.items())

nfa_tests.run_all_determinizattion()
dfa_tests.run_all_minimization()
