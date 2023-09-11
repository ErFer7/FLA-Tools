'''
Grammar.
'''

from random import choice


class Grammar():

    '''
    Grammar.
    '''

    _initial_production_rule: str
    _production_rules: dict[str, list[str]]

    def __init__(self, grammar: str) -> None:
        self._initial_production_rule = ''
        self._production_rules = {}

        lines = grammar.splitlines()

        for line in lines:
            tokens = line.strip().split()

            if len(tokens) >= 3:
                if tokens[1] != '->':
                    raise ValueError('Invalid production.')

                if tokens[0] not in self._production_rules:
                    self._production_rules[tokens[0]] = []

                    if self._initial_production_rule == '':
                        self._initial_production_rule = tokens[0]

                self._production_rules[tokens[0]] += filter(lambda x: x != '|', tokens[2:])
            else:
                raise ValueError('Invalid production.')

    def __str__(self) -> str:
        '''
        Returns a string representation of the grammar.
        '''

        string = ''

        for production_rule in self._production_rules.items():
            string += f'{production_rule[0]} -> '

            for right_hand_side in production_rule[1]:
                string += f'{right_hand_side} | '

            string = string[:-3] + '\n'

        return string

    def proccess_step(self, string: str) -> tuple[str, bool]:
        '''
        Proccesses a step.
        '''

        for left_hand_side in self._production_rules:
            if left_hand_side in string:
                return (string.replace(left_hand_side, self.derive_step(left_hand_side), 1), False)

        return (string, True)

    def derive_initial_production_rule(self) -> str:
        '''
        Derives the initial production rule.
        '''

        return self.derive_step(self._initial_production_rule)

    def derive_step(self, left_hand_side: str) -> str:
        '''
        Derives a step.
        '''

        if left_hand_side in self._production_rules:
            return choice(self._production_rules[left_hand_side])

        raise KeyError('Invalid left-hand side.')
