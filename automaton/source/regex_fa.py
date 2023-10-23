'''
Conversor de ER para AF.
'''

from source.parse_tree import ParseTree
from source.finite_automaton import FiniteAutomaton, FiniteAutomatonBuilder


class RegexToDFAConversor():

    '''
    Conversor de ER para DFA.
    '''

    @staticmethod
    def convert(regular_expression: str) -> FiniteAutomaton:
        '''
        Converte uma ER para um DFA.
        '''

        new_regular_expression = f'({regular_expression})#'
        parse_tree = RegexToDFAConversor.parse(new_regular_expression)
        followpos = parse_tree.calculate_followpos()

        return FiniteAutomatonBuilder.build_from_followpos(parse_tree.root.firstpos,
                                                           followpos, parse_tree.symbols,
                                                           parse_tree.positions_symbols,
                                                           parse_tree.last_symbol_index)

    @staticmethod
    def parse(regular_expression: str) -> ParseTree:
        '''
        Gera uma árvore de análise sintática.
        '''

        new_regular_expression = RegexToDFAConversor.add_concatenation_operator(regular_expression)

        operator_stack = []
        output_queue = []

        for character in new_regular_expression:
            match character:
                case '(':
                    operator_stack.append(character)
                case ')':
                    if len(operator_stack) > 0:
                        while operator_stack[-1] != '(':
                            output_queue.append(operator_stack.pop())

                    operator_stack.pop()
                case '|' | '*' | '.':
                    while True:
                        if len(operator_stack) > 0 and RegexToDFAConversor.precedes(operator_stack[-1], character):
                            output_queue.append(operator_stack.pop())
                        else:
                            break

                    operator_stack.append(character)
                case _:
                    output_queue.append(character)

        while len(operator_stack) > 0:
            output_queue.append(operator_stack.pop())

        return ParseTree(output_queue)

    @staticmethod
    def precedes(operator_a: str, operator_b: str) -> bool:
        '''
        Retorna verdadeiro se o operador A precede o operador B.
        '''

        match operator_a:
            case '|':
                match operator_b:
                    case '|':
                        return True
                    case '.' | '*':
                        return False
            case '.':
                match operator_b:
                    case '|' | '.':
                        return True
                    case '*':
                        return False
            case '*':
                return True

        return False

    @staticmethod
    def add_concatenation_operator(regular_expression: str) -> str:
        '''
        Adiciona o operador de concatenação à ER.
        '''

        new_regular_expression = ''

        for i, character in enumerate(regular_expression):
            if i == 0:
                new_regular_expression += character
                continue

            match character:
                case '(':
                    match regular_expression[i - 1]:
                        case '(' | '|':
                            pass
                        case ')' | '*' | _:
                            new_regular_expression += '.'
                case ')' | '|' | '*':
                    pass
                case _:
                    match regular_expression[i - 1]:
                        case '(' | '|':
                            pass
                        case ')' | '*' | _:
                            new_regular_expression += '.'

            new_regular_expression += character

        return new_regular_expression
