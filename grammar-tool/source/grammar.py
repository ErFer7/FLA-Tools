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

    @property
    def initial_production_rule(self) -> str:
        '''
        Returns the initial production rule.
        '''

        return self._initial_production_rule

    def derive_random_step(self, string: str) -> tuple[str, bool]:
        '''
        Proccesses a step.
        '''

        possible_rules = []

        for left_hand_side in self._production_rules:
            if left_hand_side in string:
                possible_rules.append(left_hand_side)

        if len(possible_rules) > 0:
            left_hand_side = choice(possible_rules)
            return (string.replace(left_hand_side, self.random_replacement(left_hand_side), 1), False)

        return (string, True)

    def derive_branching_step(self, string: str) -> tuple[list[str], bool]:
        '''
        Proccesses possible steps.
        '''

        possible_rules = []
        possible_results = []

        for left_hand_side in self._production_rules:
            if left_hand_side in string:
                possible_rules.append(left_hand_side)

        if len(possible_rules) == 0:
            return ([string], True)

        for possible_rule in possible_rules:
            for possible_replacement in self.all_replacements(possible_rule):
                possible_results.append(string.replace(possible_rule, possible_replacement, 1))

        return (possible_results, False)

    def random_replacement(self, left_hand_side: str) -> str:
        '''
        Derives a step.
        '''

        if left_hand_side in self._production_rules:
            result = choice(self._production_rules[left_hand_side])

            return result if result != 'null' else ''

        raise KeyError('Invalid left-hand side.')

    def all_replacements(self, left_hand_side: str) -> list[str]:
        '''
        Derives all possibilities.
        '''

        if left_hand_side in self._production_rules:
            return list(map(lambda x: x if x != 'null' else '', self._production_rules[left_hand_side]))

        raise KeyError('Invalid left-hand side.')
