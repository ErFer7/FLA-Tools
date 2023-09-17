'''
Testa a determinização de autômatos finitos não determinísticos.
'''

from source.finite_automaton import FiniteAutomatonBuilder, FiniteAutomatonDeterminizer


class Tests():

    '''
    Tests.
    '''

    _automata: list[tuple[str, str]]

    def __init__(self, automata: list[tuple[str, str]]) -> None:
        self._automata = automata

    def run_all(self) -> None:
        '''
        Runs the tests.
        '''

        print('Running tests\n')

        for input_nfa, output_dfa in self._automata:
            self.run(input_nfa, output_dfa)
            print()

    def run(self, input_nfa: str, output_dfa: str) -> None:
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
