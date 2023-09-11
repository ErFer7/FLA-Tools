'''
Generator.
'''

from source.grammar import Grammar


class Generator():

    '''
    Generator.
    '''

    _strings: list[str]
    _grammar: Grammar

    def __init__(self, grammar: Grammar) -> None:
        self._strings = []
        self._grammar = grammar

    @property
    def strings(self) -> list[str]:
        '''
        Returns the generated strings.
        '''

        return self._strings


    def run(self, str_count: int) -> None:
        '''
        Runs the generator.
        '''

        for _ in range(str_count):
            string = self._grammar.derive_initial_production_rule()

            while True:
                string, is_done = self._grammar.proccess_step(string)

                if is_done:
                    break

            self._strings.append(string)

        self._strings = sorted(self._strings, key=len)
