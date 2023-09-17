'''
First list.
'''

import sys
from os.path import join
from source.generator import Generator
from source.grammar import Grammar


class Tests():

    '''
    Tests.
    '''

    _depth: int

    def __init__(self, depth: int) -> None:
        self._depth = depth

    def generate_strings(self, grammar_file: str) -> list[str]:
        '''
        Generates strings.
        '''

        try:
            with open(grammar_file, 'r', encoding='utf-8') as file:
                grammar = Grammar(file.read())
        except (FileNotFoundError, ValueError) as error:
            print(error)
            sys.exit(1)

        return Generator.generate_branches(grammar, self._depth)


    def run_all(self) -> None:
        '''
        Runs the tests.
        '''

        print('Running tests')

        for i in range(1, 36):
            self.run(join('samples', f'list_{i}.txt'), lambda string: self.test_rule(string, i))

    def run(self, grammar_file: str, test_rule: callable) -> None:
        '''
        Runs the tests.
        '''

        print(f'Running tests for {grammar_file}')

        strings = self.generate_strings(grammar_file)

        for string in strings:
            if not test_rule(string):
                print(f'Failed for {string}')

        print(f'{grammar_file} passed')

    def test_rule(self, string: str, index: int) -> bool:
        '''
        Exercises.
        '''

        match index:
            case 1:
                if len(string) > 0:
                    return string[0] == string[-1]

                return True
            case 2:
                if len(string) > 0:
                    return string[0] == string[-1] and string.count('c') % 2 != 0

                return False
            case 3:
                if len(string) > 0:
                    return string[0] == string[-1] and string.count('c') % 2 != 0 and string.count('a') % 3 == 0

                return False
            case 4:
                return 'bb' in string
            case 5:
                return 'bb' not in string
            case 6:
                return string.count('b') % 2 == 0 and string.count('a') % 3 == 0
            case 7:
                return string.count('ab') == string.count('ba')
            case 8:
                return string.count('a') % 2 == 0 and string.count('b') % 2 == 0
            case 9:
                return string.count('a') % 2 == 0 and string.count('b') % 2 == 0 and string.count('c') % 2 != 0
            case 10:
                return string.startswith('a') and string.endswith('b') and string.count('c') % 2 == 0
            case 11:
                return len(string) % 2 != 0 and string.count('bb') == 0
            case 12:
                test_value = string.count('a') + string.count('c')
                return test_value % 3 == 0 and test_value != 0 and string.count('b') % 2 == 0
            case 13:
                total = 0

                for char in string:
                    total += int(char)

                return total % 4 == 0
            case 14:
                return int(f'0b{string}', 2) % 2 == 0
            case 15:
                return int(f'0b{string}', 2) % 3 == 0
            case 16:
                num = int(f'0b{string}', 2)
                return num % 2 == 0 and num % 3 == 0
            case 17:
                b_state = False

                for char in string:
                    if char == 'a' and b_state:
                        return False
                    elif char == 'b':
                        b_state = True

                return (string.count('a') + string.count('b')) % 3 == 0
            case 18:

                b_state = False
                c_state = False

                for char in string:
                    if char == 'a' and (b_state or c_state):
                        return False
                    elif char == 'b':
                        if c_state:
                            return False

                        b_state = True
                    elif char == 'c':
                        c_state = True

                return string.count('a') + string.count('c') % 3 == 0 and string.count('b') % 2 == 0
            case _:
                return False
