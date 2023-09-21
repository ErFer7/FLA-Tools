'''
Generator.
'''

from source.grammar import Grammar


class Generator():

    '''
    Generator.
    '''

    @staticmethod
    def generate_random(grammar: Grammar, str_count: int) -> list[str]:
        '''
        Runs the generator.
        '''

        strings = []

        for _ in range(str_count):
            string = grammar.initial_production_rule

            while True:
                string, is_done = grammar.derive_random_step(string)

                if is_done:
                    break

            strings.append(string)

        return sorted(strings, key=len)

    @staticmethod
    def generate_branches(grammar: Grammar, max_depth: int) -> list[str]:
        '''
        Runs the generator.
        '''

        strings = Generator.proccess_branch_step(grammar, grammar.initial_production_rule, 0, max_depth)
        return sorted(strings, key=len)

    @staticmethod
    def proccess_branch_step(grammar: Grammar, string: str, call_depth: int, max_depth: int) -> list[str]:
        '''
        Runs the generator.
        '''

        if call_depth > max_depth:
            return []

        possible_results, is_done = grammar.derive_branching_step(string)

        if is_done:
            return possible_results

        results = []

        for possible_result in possible_results:
            result = Generator.proccess_branch_step(grammar, possible_result, call_depth + 1, max_depth)

            if result is not None:
                results += result

        return results
