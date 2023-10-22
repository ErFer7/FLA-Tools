'''
Determinização.
'''

from source.finite_automaton import FiniteAutomatonBuilder, FiniteAutomatonDeterminizer


raw_nfa = input()

nfa = FiniteAutomatonBuilder.build(raw_nfa)
dfa = FiniteAutomatonDeterminizer.determinize(nfa)
print(dfa)
