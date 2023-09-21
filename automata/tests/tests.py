'''
Testa a determinização de autômatos finitos não determinísticos.
'''

from source.finite_automaton import FiniteAutomatonBuilder, FiniteAutomatonDeterminizer, FiniteAutomatonMinimizer


class Tests():

    '''
    Tests.
    '''

    _automata: list[tuple[str, str]]

    def __init__(self, automata: list[tuple[str, str]]) -> None:
        self._automata = automata

    def run_all_minimization(self) -> None:
        '''
        Runs the tests.
        '''

        print('Running tests\n')

        for input_dfa, output_dfa in self._automata:
            self.run_minimization(input_dfa, output_dfa)
            print()

    def run_all_determinizattion(self) -> None:
        '''
        Runs the tests.
        '''

        print('Running tests\n')

        for input_nfa, output_dfa in self._automata:
            self.run_determinization(input_nfa, output_dfa)
            print()

    def run_determinization(self, input_nfa: str, output_dfa: str) -> None:
        '''
        Runs the test.
        '''

        print(f'Running tests for {input_nfa}')

        nfa = FiniteAutomatonBuilder.build(input_nfa)
        dfa = FiniteAutomatonDeterminizer.determinize(nfa)

        if str(dfa) == output_dfa:
            print(f'{input_nfa} passed with result {dfa}')
        else:
            print(f'{input_nfa} failed')
            print(f'Compare:\n[Result  ]: {dfa}\n[Expected]: {output_dfa}')

    def run_minimization(self, input_dfa: str, output_dfa: str) -> None:
        '''
        Runs the test.
        '''

        print(f'Running tests for {input_dfa}')

        dfa = FiniteAutomatonBuilder.build(input_dfa)
        minimal_dfa = FiniteAutomatonMinimizer.minimize(dfa)

        if str(minimal_dfa) == output_dfa:
            print(f'{input_dfa} passed with result {minimal_dfa}')
        else:
            print(f'{input_dfa} failed')
            print(f'Compare:\n[Result  ]: {minimal_dfa}\n[Expected]: {output_dfa}')
