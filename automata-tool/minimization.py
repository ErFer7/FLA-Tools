'''
Minimização.
'''

from source.finite_automaton import FiniteAutomatonBuilder, FiniteAutomatonMinimizer


raw_dfa = input()

dfa = FiniteAutomatonBuilder.build(raw_dfa)
minimal_dfa = FiniteAutomatonMinimizer.minimize(dfa)
print(minimal_dfa)
